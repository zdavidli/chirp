from flask import Flask, render_template
import sqlite3
import ast

#flask imports
from flask import request
from flask_restful import Resource, Api
from flask import send_file


#Model imports
from model import Voice
from util import record
from util import writeWav
from util import RATE
from loader import loadVoice
from loader import loadAllVoices
from CMUDict import CMUDict


db = "../twit_data.db"

app = Flask(__name__)
api = Api(app)

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

#curl http://localhost:5000/tts/<speaker_id> -d "data=words to read out" -X GET
class tts(Resource):
  def get(self, speaker_id):
    txt = request.form['data']
    try:
      v = getVoice(speaker_id)
      counter += 1
      filename = "renderedAudio/" + speaker_id + str(counter % 10) + ".wav"
      writeWav(filename, v.tts(txt,cmu,delay=0.2))
      return send_file(filename, mimetype='audio/wav'), 200
    except:
      return " 'status': 'failed'", 500

api.add_resource(tts, '/tts/<string:speaker_id>')

#curl http://localhost:5000/train/<user_id> -d "data=<recording>" -X PUT
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

def get_top_tweets():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * from twit_data  ORDER BY datetime DESC LIMIT 30")
    result = c.fetchall()
    tweets = []

    datetime_toptweets = result[0]['datetime']

    for tweet in result:
        tweets.append(tweet['top_tweet'])

    conn.close()

    return tweets, datetime_toptweets

def get_lang():

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * from lang_data ORDER BY datetime DESC LIMIT 1")

    result = c.fetchone()
    lang = ast.literal_eval(result['language'])
    top_lang = ast.literal_eval(result['top_language'])

    conn.close()

    return lang, top_lang

@app.route("/")
def main():
    language_data = []
    top_language_data = []

    lang, top_lang = get_lang()
    for l in lang:
        language_data.append([l[0], l[1], l[1]])

    for t in top_lang:
        top_language_data.append([t[0], t[1], t[1]])
    return render_template("lang1.html", language_data = language_data, top_language_data = top_language_data)

@app.route("/top_tweets")
def top_tweets():
    tweets, datetime_toptweets = get_top_tweets()
    return render_template('top_tweets.html', tweets = tweets, datetime_toptweets = datetime_toptweets)
    
@app.route("/train")
def train():
    return render_template('train.html')

if __name__ == "__main__":
    app.run(debug = True, port=80)

