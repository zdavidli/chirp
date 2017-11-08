#flask imports
from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask import send_file


#Model imports
from model import Voice
from model import record
from model import writeWav
from loader import loadVoice
from loader import loadAllVoices

app = Flask(__name__)
api = Api(app)

# Initialize the voice data and cmudict
voices = loadAllVoices()
cmu = CMUDict()
cmu.load_dict("dict.p")
counter = 0

#curl http://localhost:5000/hello/1 -d "data=Remember the milk" -X GET
class HelloWorld(Resource):
  def get(self, todo_id):
    d = request.form['data']
    return {'hello': d}

api.add_resource(HelloWorld, '/hello/<string:todo_id>')

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

        
if __name__ == '__main__':
    app.run(debug=True)