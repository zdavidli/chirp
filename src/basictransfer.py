
import scipy.io.wavfile
import librosa

filename = 'static/audio/gary0.mp3'

y, sr = librosa.load(filename)


# rate, data = scipy.io.wavfile.read(filename)
# print rate
# print data