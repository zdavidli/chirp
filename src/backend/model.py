import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile

FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

class Voice:

	def __init__(self, id):
		self.phonemes = dict()
		self.userid = id
		
	def __hash__(self):
		return self.userid
	
	def addPhoneme(self, key, audio):
		self.phonemes[key] = self.serialize(audio)
		
	def getPhoneme(self, key):
		return self.phonemes[key]
		
	def serialize(self, input):
		return np.concatenate(input)
		
	def hard(self):
		return self.concat(self.phonemes['test'], self.phonemes['test2'], RATE * 1)
			
	def concat(self, v1, v2, i):
		combined = np.zeros(i+len(v2))
		combined[:len(v1)] = v1
		combined[i:len(v1)] /= 2
		combined[i:len(v1)] += v2[:len(v1)-i]/2
		combined[len(v1):] += v2[len(v1)-i:]
		return combined
			
	# Cut out the initial silence
	def trimFront(self, audio):
		i = 0
		sample = int(RATE / 100)
		while (volume(audio[i:i+sample:2]) < 0.5):
			i += sample * 4
		return audio[i:]
		
	def volume(self, audio):
		return sum(abs(audio)) / len(audio)
		
	def setId(self, id):
		self.userid = id
		
	def save(self):
		pickle.dump(v,open(dataroot + str(self.userid) + ".dat", 'wb'))
	
	# Text to speech
	def tts(txt):
		# TODO
		return []
		
	def textToPhonemes(txt):
		# TODO
		return []
		
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

frames = record(3)

#v.addPhoneme("test", frames)

#def bytes2int(b):
#	return int(b.encode('hex'), 16)
#for i in v.phonemes["test"][5]:
#	print str(bytes2int(i)) + ' '
#print len(v.phonemes["test"][5])
#for i in v.phonemes["test"]:
#	print i + ' '
writeWav("output.wav", v.hard())

pickle.dump(v,open("voice.dat", 'wb'))
