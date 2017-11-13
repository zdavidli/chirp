import pyaudio
import wave
import cPickle as pickle
from loader import dataroot
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os

FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100

def record(time):
  p = pyaudio.PyAudio()
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
    frames.append(np.fromstring(data, dtype=np.int16))

  print("* done recording")

  stream.stop_stream()
  stream.close()
  #p.terminate()
  return frames
  
def writeWav(filename, frames):
  wavfile.write(filename, RATE, frames)
