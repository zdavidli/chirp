import pyaudio
import wave
import cPickle as pickle


FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100
p = pyaudio.PyAudio()

class Voice:
	
	phonemes = dict()
	
	def __init__(self):
		self.phonemes = dict()
	
	def addPhoneme(self, key, audio):
		self.phonemes[key] = audio
		
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

v = pickle.load(open("voice.dat", 'rb'))

frames = record(3)

#v.addPhoneme("test", frames)

writeWav("output.wav", v.phonemes["test"])

pickle.dump(v,open("voice.dat", 'wb'))