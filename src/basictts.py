from gtts import gTTS
from pydub import AudioSegment
import wave
import os
from basictransfer import VoiceTransfer

def ttsbase(txt, file, pitch, id):
  print("Generating base voice")
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

  print("Pitcing voice")
  fileext = "mod.wav"
  hastraining = os.path.isfile("static/traindata/" + str(id) + "/0.wav")
  if hastraining == False:
    fileext = "trans.wav"
  wf = wave.open(file + fileext, 'wb')
  print("here")
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(swidth)
  wf.setframerate(RATE*Change_RATE)
  wf.writeframes(signal)
  wf.close()

if __name__ == "__main__":
  ttsbase("It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",  "static/audio/gary.", 0.85, "gary")