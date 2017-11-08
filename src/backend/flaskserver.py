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

voices = loadAllVoices()


#curl http://localhost:5000/hello/1 -d "data=Remember the milk" -X GET
class HelloWorld(Resource):
  def get(self, todo_id):
    d = request.form['data']
    return {'hello': d}

api.add_resource(HelloWorld, '/hello/<string:todo_id>')


'''@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/gif')'''

class tts(Resource):
  def get(self, speaker_id):
    filename = 'output.wav'
    userid = request.form['data']
    return send_file(filename, mimetype='audio/wav')

api.add_resource(tts, '/tts/<string:speaker_id>')



'''@app.route("/")
def hello():
  return "Hello World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    do_the_login()
  else:
    show_the_login_form()'''
        
if __name__ == '__main__':
    app.run(debug=True)