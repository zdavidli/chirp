import pyaudio
import wave
import cPickle as pickle
import loader
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
from CMUDict import CMUDict, ALL_PHONEMES, exampleWords
from util import record
from util import writeWav
from util import RATE
from model import Voice
import sys
import argparse


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

TRAIN_VOCAB = ALL_PHONEMES#['W', 'ER', 'L', 'D']

cmuDict = CMUDict()
cmuDict.load_dict("dict.p")


def get_args():
	parser = argparse.ArgumentParser(description='Train a voide model')
	parser.add_argument('--user', dest='user', type=str)
	#parser.add_argument('--overwrite', dest = 'overwrite', default=False, type=bool)
	return parser


def train_model(model, phonemes=ALL_PHONEMES):
	for phone in phonemes:
		accepted = False
		#while not accepted:
		print "Please say the phoneme %s as in %s or %s" % (phone, exampleWords[phone][0],exampleWords[phone][1])
		raw_input("Press enter to start recording")
		audio = record(1.2)
			#accepted = raw_input("Accept Recording? y/n:\n") == 'y'
			#print accepted
		try:
			model.addPhoneme(phone, audio)
		except:
			print "Please rerecord"
	return model

def main():
	args =get_args().parse_args()
	voice = loader.loadVoice(args.user)
	if voice == None:
		print "Creating new voice model"
		voice = Voice(args.user)
		train_model(voice, TRAIN_VOCAB)
	else:
		untrained = len(voice.missingPhonemes())
		print "User already exist with %d untrained phonemes" % untrained
		if untrained >0 and raw_input("Continue training? (y/n): \n")=='y':
			voice = train_model(voice, phonemes=voice.missingPhonemes())
		elif untrained == 0 and raw_input("Overwrite all phonemes? (y/n): \n") =='y':
			retrain_model(voice)
		else:
			phone = raw_input("Type a phoneme to rerecord (type q to finish:\n")
			while phone is not 'q':
				if phone in ALL_PHONEMES:
					train_model(voice, [phone])
				else:
					print "Invalid phoneme"
				phone = raw_input("Type a phoneme to rerecord (type q to finish:\n")
	voice.save()












if __name__ == '__main__':
	main()

