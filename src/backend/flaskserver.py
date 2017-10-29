#flask imports
from flask import Flask
from flask import request
#Model imports
from model import Voice
from model import record
from model import writeWav
from loader import loadVoice
from loader import loadAllVoices

app = Flask(__name__)

voices = loadAllVoices()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()