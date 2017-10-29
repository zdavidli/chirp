import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
from CMUDict import CMUDict


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
cmudict = CMUDict()
cmudict.load_dict("dict.p")

class Voice:

	def __init__(self, id):
		self.phonemes = dict()
		self.userid = id
		if self.userid+"_PhonemeBank" not in os.listdir(os.path.abspath("VoiceData/")):
			self.generatePhonemeDict()
		#else if len(os.listdir(os.path.abspath("VoiceData/"+self.userid+"_PhonemeBank"))) < 44:
		#	self.generatePhonemeDict()
		
	def __hash__(self):
		return self.userid
	
	def generatePhonemeDict(self):
			pronounce_dict = {}
			with open("cmudict.pronounciations", "r") as infile:
			    for line in infile.readlines():
			        line = line.split("\t")
			        line[2] = line[2].rstrip("\n")
			        pronounce_dict[line[0]] = line[1:]

			for phoneme in sorted(cmudict.get_phonemes()):
				print("Pronounce " + phoneme + " like " + phoneme + " in " \
					+ pronounce_dict[phoneme][0] + " (Spelled " \
					+ pronounce_dict[phoneme][1] + "). ENTER when done.")
				  
				self.addPhoneme(phoneme, record(3))
				_listener = raw_input("Hit ENTER to continue.")
				writeWav("id"+phoneme+".wav", self.phonemes[phoneme])

	def addPhoneme(self, key, audio):
		self.phonemes[key] = self.normalize(self.trimBack(self.trimFront(self.serialize(audio))))
		
	def getPhoneme(self, key):
		return self.phonemes[key]
		
	def serialize(self, input):
		return np.concatenate(input)
		
	def renderWord(self, pron):
		out = self.phonemes[pron[0][0]]
		for i in range(1,len(pron)):
			out = self.concat(out, self.phonemes[pron[i][0]], RATE * 0.1)
			print len(out)
		return out

	def concat(self, v1, v2, i=0):
		i = int(min(i, len(v1)))
		v1, v2 = v1.astype(np.int32), v2.astype(np.int32)
		left = v1[:len(v1) - i]
		right = []
		m1 = []
		m2 = []
		if i >= len(v2):
			right = v1[len(v1) - i:len(v1) - i + len(v2)]
			m1 = v1[len(v1) - i:len(v1) - i + len(v2)]
			m2 = v2
		else:
			right = v2[i:]
			m1 = v1[len(v1) - i:]
			m2 = v2[:i]
		m1 = m1[:len(m2)] + m2
		m1[m1>32767] = 32767
		m1[m1<-32767] = -32767
		return np.append(np.append(left, m1), right).astype(np.int16)
		'''v1,v2 = v1.astype(np.int32), v2.astype(np.int32)
		combined = np.zeros(max(i+len(v2), len(v1)))
		combined[:len(v1)] = v1
		combined[i:i+len(v2)] += v2
		combined[combined>32767] = 32767
		combined[combined<-32767] = -32767'''
		return combined.astype(np.int16)
		
	def normalize(self, audio):
		mean = np.mean(np.abs(audio)) * 2
		ratio = mean / 4000.0
		return (audio / ratio).astype(np.int16)
			
	# Cut out the initial silence
	def trimFront(self, audio):
		i = 0
		sample = int(RATE / 100)
		while (self.volume(audio[i:i+sample:2]) < 1500):
			i += sample * 4
		return audio[i:]
		
	def trimBack(self, audio):
		i = len(audio) - 1
		sample = int(RATE / 100)
		while (self.volume(audio[i-sample:i:2]) < 1500):
			i -= sample * 4
		return audio[:i]
		
	def volume(self, audio):
		return np.sum(abs(audio)) / len(audio)
		
	def setId(self, id):
		self.userid = id
		
	def save(self):
		pickle.dump(v,open(dataroot + str(self.userid) + ".dat", 'wb'))
	
	# Text to speech
	def tts(self,txt):
		# TODO
		return []
		
	def textToPhonemes(self, txt):
		phonemes = []
		'''for word in text.split(" "):
			wordPhones = self.cmudict.getPhoneme(word)[0]
			wordPhones = reduce(lambda x,y: x + y[0], self.cmudict.getPhoneme(word)[0], [])
			phonemes += wordPhones + [" "]'''
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
#v.addPhoneme('K', frames)
world = [('W', 0), ('ER', '1'), ('L', 0), ('D', 0)]
scott = [('S', 0), ('K', 0), ('AA', 1), ('T', 0)]
hello = [('HH',0), ('EH',0), ('L',0), ('OW',0)]
writeWav("output.wav", np.concatenate((v.renderWord(hello),np.zeros((RATE * 0.2)).astype(np.int16),v.renderWord(scott))))

pickle.dump(v,open("voice.dat", 'wb'))
