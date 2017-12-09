#!/usr/bin/env python
import array
import argparse
import ast
import cgitb
import cgi
import numpy as np
import os
import os.path
import requests
import os
import sqlite3
from twython import Twython
import wave

#flask imports
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask import send_file
from flask_restful import Resource, Api
from flask import send_from_directory

#config import
import config

#Model imports
from model import Voice
from util import record
from util import writeWav
from util import RATE
from loader import loadVoice
from loader import loadAllVoices
from CMUDict import CMUDict

db = "./twit_data.db"

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.urandom(24)
twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth = twitter.get_authentication_tokens(callback_url='localhost:5000/callback')
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']



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
voices = loadAllVoices()
cmu = CMUDict()
cmu.load_dict("dict.p")
counter = 0
cgitb.enable()

#curl http://localhost:5000/samplerate -d "data=Remember the milk" -X GET
class SampleRate(Resource):
  def get(self):
    return {'rate': RATE}, 200

api.add_resource(SampleRate, '/samplerate')

# Get the voice by the id. If the voice is not loaded, load it.
# if the voice does not exist, return DEFAULT
def getVoice(speaker_id):
  if speaker_id in voices:
    return voices[speaker_id]
  else:
    v = loadVoice(speaker_id)
    if v is None:
      return voices['DEFAULT']
    else:
      voices[speaker_id] = v
      return voices[speaker_id]

def getCount():
  counter += 1
  return counter

#curl http://localhost/tts/<speaker_id> -d "words to read out" -X GET
@app.route('/api/tts/<string:speaker_id>', methods=['GET', 'POST'])
def tts(speaker_id):
  txt = request.values.keys()[0]
  if txt is None:
    print "Text was None. Falling back"
    txt = "fallback text to render"
    #return " 'status': 'No text'", 400
  try:
    v = getVoice(speaker_id)
    renderroot = "static/audio/"
    counter = 0
    filename = renderroot + speaker_id + str(counter) + ".wav"

    audio = v.tts(txt,cmu,delay=0.2)
    #print audio
    writeWav(filename, audio)
    return filename, 200
  except:
    return "'status': 'failed'", 500

@app.route('/api/addtraindata/<string:speaker_id>', methods=['POST', 'PUT'])
def addtraindata(speaker_id):
  #txt = request.values.keys()[0]
  try:
    root = "static/traindata/" + speaker_id
    counter = 0
    filename = root + "/" + str(counter) + ".wav"
    while os.path.isfile(filename) == True:
      counter += 1
      filename = root + "/" + str(counter) + ".wav"
    if not os.path.exists(root):
      os.makedirs(root)
    print "Saving: " + filename
    blob = request.files['file']
    blob.save(filename)
    return "success", 200
  except Exception as e:
    print e
    return "'status': 'failed'", 500

@app.route('/api/deletetraindata/<string:speaker_id>', methods=['POST', 'PUT'])
def deletetraindata(speaker_id):
  #txt = request.values.keys()[0]
  try:
    root = "static/traindata/" + speaker_id + "/"
    counter = 0
    filename = root + str(counter) + ".wav"
    while os.path.isfile(filename) == True:
      os.remove(filename)
      counter += 1
      filename = root + str(counter) + ".wav"
    return "success", 200
  except:
    return "'status': 'failed'", 500

@app.route('/api/numsamples/<string:speaker_id>', methods=['GET'])
def numsamples(speaker_id):
  try:
    root = "static/traindata/" + speaker_id
    counter = 0
    filename = root + "/" + str(counter) + ".wav"
    while os.path.isfile(filename) == True:
      counter += 1
      filename = root + "/" + str(counter) + ".wav"
    return str(counter), 200
  except Exception as e:
    print e
    return '0', 500

@app.route('/api/train/<string:user_id>', methods=['POST', 'PUT'])
def starttrain(user_id):
  #txt = request.values.keys()[0]
  try:
    root = "static/traindata/" + user_id + "/"
    filename = root + str(counter) + ".wav"
    #train here
    return "Success: Training", 200
  except:
    return "Internal Server Error", 500

#curl http://localhost/train/<user_id> -d "data=<recording>" -X PUT
class trainer(Resource):
  def put(self, user_id):
    audio = request.form['data']
    if user_id not in voices:
      voices[user_id] = Voice()
    v = voices[speaker_id]
    try:
      v.addPhoneme(audio)
    except:
      return " 'status': 'failed'", 500
    v.save()
    return send_file(filename, mimetype='audio/wav'), 200
api.add_resource(trainer, '/train/<string:user_id>')

###################################################################################
###################################################################################
###################################################################################
#                                                                                 #
#                                 FRONTEND                                        #
#                                                                                 #
###################################################################################
###################################################################################
###################################################################################


def getArticle():
    text = []
    with open('article.txt','r') as f:
        data = f.readlines()
        for i in data:
            if i != '\n':
                text.append(i)
    return text

@app.route('/', methods=["POST"])
def index_login():
    twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth = twitter.get_authentication_tokens(callback_url='http://localhost:5000/login')
    session['OAUTH_TOKEN'] = auth['oauth_token']
    session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
    return redirect(auth['auth_url'])

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    oauth_verifier = request.args.get('oauth_verifier')
    OAUTH_TOKEN = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    session['OAUTH_TOKEN'] = final_step['oauth_token']
    session['OAUTH_TOKEN_SECRET'] = final_step['oauth_token_secret']
    OAUTH_TOKEN = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    #session['twitter'] = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return redirect('/train')

@app.route("/train")
def train():
    OAUTH_TOKEN = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    twitter.update_status(status="Twython works!")
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
