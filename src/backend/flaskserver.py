#flask imports
from flask import Flask
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

app = Flask(__name__)
api = Api(app)

# Initialize the voice data and cmudict
voices = loadAllVoices()
cmu = CMUDict()
cmu.load_dict("dict.p")
counter = 0

#curl http://localhost:5000/samplerate -d "data=Remember the milk" -X GET
class SampleRate(Resource):
  def get(self):
    return {'rate': RATE}

api.add_resource(SampleRate, '/samplerate')

#curl http://localhost:5000/tts/<speaker_id> -d "data=words to read out" -X GET
class tts(Resource):
  def get(self, speaker_id):
    txt = request.form['data']
    v = voices[speaker_id]
    counter += 1
    filename = "renderedAudio/" + speaker_id + str(counter % 10) + ".wav"
    writeWav(filename, v.tts(txt,cmu,delay=0.2))
    return send_file(filename, mimetype='audio/wav')

api.add_resource(tts, '/tts/<string:speaker_id>')

#curl http://localhost:5000/train/<user_id> -d "data=<recording>" -X PUT
class trainer(Resource):
  def put(self, user_id):
    audio = request.form['data']
    if user_id not in voices:
      voices[user_id] = Voice()
    v = voices[speaker_id]
    v.addPhoneme(audio)
    v.save()
    return send_file(filename, mimetype='audio/wav')

api.add_resource(trainer, '/train/<string:user_id>')

        
if __name__ == '__main__':
    app.run(debug=True)