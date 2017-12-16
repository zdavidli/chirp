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

  print("Transferring")
  if hastraining == True:
    obj = VoiceTransfer(id)
    obj.transfer()

if __name__ == "__main__":
  ttsbase("testing one two three four five six seven eight nine ten the is a sentence that is rather long for demonstration purposes otherwise we would try to make shorter sentences because it is faster",  "static/audio/gary.", 0.85, "gary")