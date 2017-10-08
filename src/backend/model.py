import pyaudio
import wave
import cPickle as pickle
from loader import dataroot

FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

class Voice:

	def __init__(self, id):
		self.phonemes = dict()
		self.userid = id
		
	def __hash__(self):
		return self.userid
	
	def addPhoneme(self, key, audio):
		self.phonemes[key] = trimFront(audio)
	
	# Cut out the initial silence
	def trimFront(self, audio):
		i = 0
		sample = int(RATE / 100)
		while (volume(audio[i:i+sample:2] < 0.5):
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
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
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

#v.addPhoneme("test", frames)

writeWav("output.wav", v.phonemes["test"])

pickle.dump(v,open("voice.dat", 'wb'))