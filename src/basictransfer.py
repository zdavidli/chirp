
import numpy as np
import pickle
import os
import os.path
import librosa

from basictts import  ttsbase

def pitchFromData(user_id):
	filebase = "static/traindata/" + user_id+ "/"
	counter = 0
	totPitch = 0
	files = 0
	while (True):
		filename = filebase + str(counter) + ".wav"
		if (os.path.isfile(filename) == False):
			break
		y, sr = librosa.load(filename, sr=40000)
		pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, fmin=75, fmax=1600)

		np.set_printoptions(threshold=np.nan)
		s = 0
		i = 0
		for t in range(0, pitches.shape[1], 3):
			# print magnitudes[:,t].mean()
			if (magnitudes[:,t].mean() > 0.03):
				s += detect_pitch(pitches, magnitudes, t)
				i += 1
		if (i != 0):
			totPitch += s / i
			files += 1
		counter += 1
	pitch = totPitch / files
	pickle.dump(pitch, open("static/pitches/" + user_id, "wb"))
	return pitch



def detect_pitch(pitches, magnitudes, t):
  index = magnitudes[:, t].argmax()
  pitch = pitches[index, t]

  return pitch