import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
from CMUDict import CMUDict
from util import record
from util import writeWav
from util import RATE
from model import Voice

#v = Voice("12345")
v = pickle.load(open("voice.dat", 'rb'))

#frames = record(1)
#v.addPhoneme('K', frames)
world = [('W', 0), ('ER', '1'), ('L', 0), ('D', 0)]
scott = [('S', 0), ('K', 0), ('AA', 1), ('T', 0)]
hello = [('HH',0), ('EH',0), ('L',0), ('OW',0)]
writeWav("output.wav", np.concatenate((v.renderWord(hello),np.zeros((RATE * 0.2)).astype(np.int16),v.renderWord(scott))))

pickle.dump(v,open("voice.dat", 'wb'))