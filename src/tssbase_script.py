from gtts import gTTS
from pydub import AudioSegment
import wave
import os
from basictransfer import VoiceTransfer

def ttsbase(args):
  print("1. Generating base voice using Google TTS")
  tts = gTTS(text=args.txt, lang='en', slow=False)
  tts.save(args.content_dir+args.userId+".mp3")
  baseVoice = AudioSegment.from_mp3(args.content_dir+args.userId+"mp3")
  baseVoice.export(args.content_dir + "wav", format="wav")
  spf = wave.open(args.content_dir + "wav", 'rb')

  print("2. Adjusting pitch of base voice")
  assert os.path.isfile(args.style_dir + str(args.userId) + "/0.wav") == True
  wf = wave.open(args.content_dir + args.userId + args.fileext, 'wb')
  wf.setnchannels(args.channels)
  wf.setsampwidth(args.sWidth)
  wf.setframerate(spf.getframerate()*args.pitch) # rate * pitch
  wf.writeframes(spf.readframes(-1)) # signal
  wf.close()

  print("3. Beginning Voice Neural Style Transfer")
  obj = VoiceTransfer(args.userId, args.content_dir, args.style_dir, args.N_FILTERS, args.ALPHA, args.ITER)
  obj.transfer()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Train a U-Net model",
                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--txt', type=str, help='Input text.', default='It was a bright cold day in April, and the clocks were striking thirteen.')
  parser.add_argument('--content_dir', type=str, help='Target voice directory.', default='static/audio/')
  parser.add_argument('--style_dir', type=str, help='Style voice directory.', default='static/traindata/')
  parser.add_argument('--N_FILTERS', type=int, default=4096)
  parser.add_argument('--ALPHA', type=float, default=1e-1)
  parser.add_argument('--ITER', type=int, default=30)
  parser.add_argument('--pitch', type=float, help='Adjusted pitch', default=0.85)
  parser.add_argument('--userId', type = str, help = 'User Id', default = "gary")
  parser.add_argument('--channels', type = int, help = 'channels', default = 1)
  parser.add_argument('--sWidth', type = int, help = 'swidth', default = 2)

  args = parser.parse_args(args)
  ttsbase(args)  