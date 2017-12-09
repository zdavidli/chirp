from gtts import gTTS

def ttsbase(txt, file):
	tts = gTTS(text=txt, lang='en', slow=False)
	tts.save(file)