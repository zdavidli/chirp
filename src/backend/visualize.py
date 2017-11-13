import wave
import matplotlib.pyplot as plt
import sys
import numpy as np

wav = wave.open(sys.argv[1], 'r')
signal = wav.readframes(-1)
signal = np.fromstring(signal, 'Int16')

plt.plot(signal)
plt.show()