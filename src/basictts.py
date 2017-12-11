from gtts import gTTS
from pydub import AudioSegment
import wave

def ttsbase(txt, file, pitch):
	tts = gTTS(text=txt, lang='en', slow=False)
	tts.save(file + "mp3")
	sound = AudioSegment.from_mp3(file + "mp3")
	sound.export(file + "wav", format="wav")
	CHANNELS = 1
	swidth = 2
	Change_RATE = pitch

	spf = wave.open(file + "wav", 'rb')
	RATE=spf.getframerate()
	signal = spf.readframes(-1)

	wf = wave.open(file + "mod.wav", 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(swidth)
	wf.setframerate(RATE*Change_RATE)
	wf.writeframes(signal)
	wf.close()