import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np

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
		return self.deserialize(self.phonemes[key])
		
	def serialize(self, input):
		result = np.ndarray((len(input) * CHUNK,)).astype(np.int16)
		for (i, chunk) in enumerate(input):
			intchunk = []
			for b in chunk:
				intchunk.append(int(b.encode('hex'), 16))
			one = np.array(intchunk[::2]).astype(np.int16)
			two = np.array(intchunk[1::2]).astype(np.int16)
			print " "
			print two[0]
			print one[0]
			two = one + (256 * two)
			result[i * CHUNK:(i + 1) * CHUNK] = two
			print result[i * CHUNK]
		return result.astype(np.int16)
			
	def deserialize(self, input):
		result = np.ndarray((int(len(input) / CHUNK), CHUNK * 2))
		for i in range(int(len(input) / CHUNK)):
			one = (input[i * CHUNK:(i + 1) * CHUNK] / 256).astype(np.int8)
			two = (input[i * CHUNK:(i + 1) * CHUNK] % 256).astype(np.int8)
			result[i][::2] = two
			result[i][1::2] = one
		out = []
		for i in range(len(result)):
			out.append(str(bytearray(result[i])))
		return out
			
			
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
		frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	#p.terminate()
	return frames
	
def writeWav(filename, frames):
	wf = wave.open("outut.wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	
#v = Voice("12345")
v = pickle.load(open("voice.dat", 'rb'))

frames = record(3)

v.addPhoneme("test", frames)

#def bytes2int(b):
#	return int(b.encode('hex'), 16)
#for i in v.phonemes["test"][5]:
#	print str(bytes2int(i)) + ' '
#print len(v.phonemes["test"][5])
#for i in v.phonemes["test"]:
#	print i + ' '
writeWav("output.wav", v.getPhoneme("test"))

pickle.dump(v,open("voice.dat", 'wb'))