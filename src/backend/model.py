import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile
from CMUDict import CMUDict


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
DICT_FILE = 'dict.p'
cmudict = CMUDict().load(DICT_FILE)

class Voice:

	def __init__(self, id):
		self.phonemes = dict()
		self.userid = id
		
	def __hash__(self):
		return self.userid
	
	def addPhoneme(self, key, audio):
		self.phonemes[key] = self.trimBack(self.trimFront(self.serialize(audio)))
		
	def getPhoneme(self, key):
		return self.phonemes[key]
		
	def serialize(self, input):
		return np.concatenate(input)
		
	def renderWord(self, pron):
		out = self.phonemes[word[0]]
		for i in range(1,len(word)):
			out = self.concat(out, self.phonemes[pron[i][0]], int(len(self.phonemes[word[i-1]]) / 1.2))
		return out
			
	def concat(self, v1, v2, i=-1):
		if i < 0:
			i = len(v1) - 1
		v1,v2 = v1.astype(np.int32), v2.astype(np.int32)
		combined = np.zeros(i+len(v2))
		combined[:len(v1)] = v1
		combined[i:] += v2
		combined[combined>32767] = 32767
		combined[combined<-32767] = -32767
		return combined.astype(np.int16)
			
	# Cut out the initial silence
	def trimFront(self, audio):
		i = 0
		sample = int(RATE / 100)
		while (self.volume(audio[i:i+sample:2]) < 1000):
			i += sample * 4
		return audio[i:]
		
	def trimBack(self, audio):
		i = len(audio) - 1
		sample = int(RATE / 100)
		while (self.volume(audio[i-sample:i:2]) < 1000):
			i -= sample * 4
		return audio[:i]
		
	def volume(self, audio):
		return np.sum(abs(audio)) / len(audio)
		
	def setId(self, id):
		self.userid = id
		
	def save(self):
		pickle.dump(v,open(dataroot + str(self.userid) + ".dat", 'wb'))
	
	# Text to speech
	def tts(txt):
		# TODO
		return []
		
	def textToPhonemes(txt):
		phonemes = []
		for word in text.split(" "):
			wordPhones = self.cmudict.getPhoneme(word)[0]
			wordPhones = reduce(lambda x,y: x + y.keys[0], self.cmudict.getPhoneme(word)[0], [])
			phonemes += wordPhones + [" "]
		return phonemes
		
def record(time):
	RECORD_SECONDS = time


	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(np.fromstring(data, dtype=np.int16))

	print("* done recording")
	print np.max(frames)

	stream.stop_stream()
	stream.close()
	#p.terminate()
	return frames
	
def writeWav(filename, frames):
	wavfile.write(filename, RATE, frames)

	
#v = Voice("12345")
v = pickle.load(open("voice.dat", 'rb'))

#frames = record(1)

#v.addPhoneme('L', frames)

writeWav("output.wav", v.renderWord([('HH',0), ('EH',0), ('L',0), ('OW',0)]))

pickle.dump(v,open("voice.dat", 'wb'))
