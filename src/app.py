#!/usr/bin/env python
import array
import argparse
import ast
import cgitb
import cgi
import json
import numpy as np
import os
import requests
import sqlite3
from twython import Twython
import wave
import pickle
import librosa

#flask imports
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask import send_file
from flask_restful import Resource, Api
from flask import send_from_directory


#twitter frontend imports
import twitter_api as tapi
import twitter_login as tl

#config import
import config

#Model imports
from util import RATE
from loader import loadVoice
from loader import loadAllVoices
from loader import VoiceIO
from loader import VoiceDB
from CMUDict import CMUDict
from basictts import ttsbase
from basictransfer import pitchFromData

db = "./twit_data.db"

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.urandom(24)
twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth = twitter.get_authentication_tokens(callback_url='localhost:5000/callback')
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']


GooglePitch = 439.0
# ttsbase("It was a bright cold day in April and the clocks were striking thirteen Winston Smith his chin nuzzled into his breast in an effort to escape the vile wind slipped quickly through the glass doors of Victory Mansions though not quickly enough to prevent a swirl of gritty dust from entering along with him", "static/traindata/google/0.wav", 1)


###################################################################################
###################################################################################
###################################################################################
#                                                                                 #
#                                 BACKEND                                         #
#                                                                                 #
###################################################################################
###################################################################################
###################################################################################

# Initialize the voice data and cmudict
db = VoiceDB()
# cmu = CMUDict()
# cmu.load_dict("dict.p")
counter = 0
cgitb.enable()
#Initialize VoiceIO
voiceIO = VoiceIO()

peopleTraining = set()

# delete all temp voice data
for filename in os.listdir("static/audio"):
  if filename.endswith(".wav") or filename.endswith(".mp3"):
    os.remove(os.path.join("static/audio", filename))
    continue
  else:
    continue

#curl http://localhost:5000/samplerate -d "data=Remember the milk" -X GET
class SampleRate(Resource):
  def get(self):
    return {'rate': RATE}, 200

api.add_resource(SampleRate, '/samplerate')

#curl http://localhost/tts/<speaker_id> -d "words to read out" -X GET
@app.route('/api/tts/<string:speaker_id>', methods=['GET', 'POST'])
def tts(speaker_id):
  txt = request.values['message']
  print(txt)
  if txt is None:
    print("Text was None. Falling back")
    txt = "fallback text to render"
    #return " 'status': 'No text'", 400
  try:
    renderroot = "static/audio/"
    counter = 0
    filename = renderroot + speaker_id + "."
    print(filename)

    # pFilename = "static/pitches/" + speaker_id
    # pitch = GooglePitch
    # if os.path.isfile(pFilename):
    #   pitch = pickle.load(open(pFilename, 'rb'))
    #   print("Loaded")
    # print(pitch)
    print("Getting model")
    m = db.getModel(speaker_id)
    print("Performing TTS")
    m.tts(txt, filename)
    #ttsbase(txt, filename, pitch / GooglePitch, speaker_id)
    print("Rendered Audio")
    out = {'filename': filename + "trans.wav", 'pitch': m.pitch / m.googlePitch}
    r = json.dumps(out)
    return r, 200
  except Exception as e:
    print(e)
    return "'status': 'failed'", 500

@app.route('/api/addtraindata/<string:speaker_id>', methods=['POST', 'PUT'])
def addtraindata(speaker_id):
  #txt = request.values.keys()[0]
  try:
    filename = voiceIO.getNextTrainFile(speaker_id)
    print("Saving: " + filename)
    blob = request.files['file']
    blob.save(filename)
    x, fs = voiceIO.loadWav(filename)
    fft=librosa.stft(x)
    bp=fft[:]
    thresh = min(800, len(bp))
    for i in range(thresh, len(bp)):
      bp[i]=0
    x=librosa.istft(bp)
    voiceIO.saveWav(speaker_id, x, fs, filename)
    return "success", 200
  except Exception as e:
    print(e)
    return "'status': 'failed'", 500

@app.route('/api/deletetraindata/<string:speaker_id>', methods=['POST', 'PUT'])
def deletetraindata(speaker_id):
  #txt = request.values.keys()[0]
  success = voiceIO.deleteTrainData(speaker_id)
  if success:
    return "success", 200
  else:
    return "'status': 'failed'", 500

@app.route('/api/numsamples/<string:user_id>', methods=['GET'])
def numsamples(user_id):
  try:
    counter = voiceIO.numSamples(user_id)
    return str(counter), 200
  except Exception as e:
    print(e)
    return '0', 500

@app.route('/api/train/<string:user_id>', methods=['POST', 'PUT'])
def starttrain(user_id):
  #txt = request.values.keys()[0]
  try:
    #root = "static/traindata/" + user_id + "/"
    #filename = root + str(counter) + ".wav"
    filename = voiceIO.getNextTrainFile(user_id)
    peopleTraining.add(user_id)
    pitchFromData(user_id)
    peopleTraining.remove(user_id)
    return "Success: Training", 200
  except:
    return "Internal Server Error", 500

@app.route('/api/istraining/<string:user_id>', methods=['GET'])
def istraining(user_id):
  #txt = request.values.keys()[0]
  try:
    status = False
    if (user_id in peopleTraining):
      status = True
      return "true", 200
    return "false", 200
  except:
    return "Internal Server Error", 500

# Returns true if the user has ever sent any training data before
@app.route('/api/hasdata/<string:speaker_id>', methods=['GET'])
def hasdata(speaker_id):
  try:
    root = "static/traindata/" + speaker_id
    exists = os.path.exists(root);
    return str(exists), 200
  except Exception as e:
    print(e)
    return 'false', 500

# Returns true if the audio rendered 
@app.route('/api/audioready/<string:speaker_id>', methods=['GET'])
def audioready(speaker_id):
  try:
    filename = "static/audio/" + speaker_id + ".trans.wav"
    exists = os.path.isfile(filename);
    return str(exists), 200
  except Exception as e:
    print(e)
    return 'false', 500

# class trainer(Resource):
#   def put(self, user_id):
#     audio = request.form['data']
#     if user_id not in voices:
#       voices[user_id] = Voice()
#     v = voices[speaker_id]
#     try:
#       v.addPhoneme(audio)
#     except:
#       return " 'status': 'failed'", 500
#     v.save()
#     return send_file(filename, mimetype='audio/wav'), 200
# api.add_resource(trainer, '/train/<string:user_id>')

###################################################################################
###################################################################################
###################################################################################
#                                                                                 #
#                                 FRONTEND                                        #
#                                                                                 #
###################################################################################
###################################################################################
###################################################################################


"""
API ENDPOINTS
"""

@app.route('/api/messages/', defaults={'count':10})
@app.route('/api/messages/<int:count>', methods=['GET'])
def get_messages(count):
    return tapi.get_messages(count, session)

@app.route('/api/feed/', defaults={'count':10})
@app.route('/api/feed/<int:count>', methods=['GET'])
def get_feed(count):
    return tapi.get_feed(count, session)

@app.route('/api/user_id', methods=["GET"])
def get_user_id():
    return tapi.get_user_id(session)

"""
LOGIN
"""

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/', methods=["POST"])
def index_login():
    twitter, auth = tl.login_button(callback='http://localhost:5000/login')
    session['OAUTH_TOKEN'] = auth['oauth_token']
    session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
    return redirect(auth['auth_url'])


@app.route('/login')
def login():
    oauth_verifier = request.args.get('oauth_verifier')

    #Set OAUTH keys
    tl.first_login(session, oauth_verifier)

    #login with updated OAUTH keys
    twitter = tl.login(session)

    response = twitter.get("account/verify_credentials")
    speaker_id = response[u"id_str"]
    exists = os.path.exists(os.path.join('./static/traindata/', speaker_id))

    url = '/train' if not exists else '/home'
    return redirect(url)

@app.route("/train")
def train():
    def getArticle():
        text = []
        with open('article.txt','r') as f:
            for line in f:
                text.append(line)
        return text

    twitter = tl.login(session)
    articles = getArticle()
    return render_template('train.html', articles = articles)


@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Specify port number for app", type=int, default=5000)
    arg = parser.parse_args()
    port_number = arg.port
    app.run(debug = True, port=port_number)
