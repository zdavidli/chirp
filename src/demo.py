import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
from CMUDict import CMUDict
from util import record
from util import writeWav
from util import RATE
from model import Voice
import sys


"""
v = pickle.load(open("voice.dat", 'rb'))

testset = pickle.load(open("testset.dat", 'rb'))
testset["OW"] = v.phonemes["OW"]
pickle.dump(testset,open("testset.dat", 'wb'))

#v = Voice("12345")
cmu = CMUDict()
cmu.load_dict("dict.p")
#frames = record(1)
#v.addPhoneme('K', frames)
world = [('W', 0), ('ER', '1'), ('L', 0), ('D', 0)]
scott = [('S', 0), ('K', 0), ('AA', 1), ('T', 0)]
hello = [('HH',0), ('EH',0), ('L',0), ('OW',0)]
#writeWav("output.wav", np.concatenate((v.renderWord(hello),np.zeros((RATE * 0.2)).astype(np.int16),v.renderWord(scott))))
writeWav("output.wav", v.tts("hello scott. hot. lot cot. hell", cmu))

#pickle.dump(v,open("voice.dat", 'wb'))
"""

cmuDict = CMUDict()
cmuDict.load_dict("dict.p")

def train_model():
	v = Voice("demo")
	for phone in cmuDict.phonemes:
		accepted = False
		while not accepted:
			print "Please say the phoneme %s" % phone
			raw_input("Press enter to start recording")
			audio = record(1)
			accepted = raw_input("Accept Recording? y/n") == 'y'
		v.addPhoneme(phone, audio)
	return v

def main():
	if len(sys.argv) >= 2:
		try:
			voice = pickle.load(open(sys.argv[1],'r'))
		except:
			print "Invalid voice model"
			exit(1)
	else:
		voice = train_model()
		voice.save()

	while True:
		writeWav("output.wav", voice.tts(raw_input("Enter word to say: \n")))
		chunk = 1024
		wav = wave.open("outpu.wav", 'r')
		p = pyaudio.PyAudio()
		stream = p.open(format =
		                p.get_format_from_width(wav.getsampwidth()),
		                channels = wav.getnchannels(),
		                rate = wav.getframerate(),
		                output = True)
		data = wav.readframes(chunk)

		# play stream (looping from beginning of file to the end)
		while data != '':
		    # writing to the stream is what *actually* plays the sound.
		    stream.write(data)
		    data = wav.readframes(chunk)

		# cleanup stuff.
		stream.close()    
		p.terminate()


if __name__ == '__main__':
	main()

