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

class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}

api.add_resource(HelloWorld, '/hello')


'''@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/gif')'''

class tts(Resource):
  def get(self):
    filename = 'output.wav'
    return send_file(filename, mimetype='audio/wav')

api.add_resource(tts, '/tts')



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