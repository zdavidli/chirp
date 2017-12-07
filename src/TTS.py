import pyaudio
import wave
import cPickle as pickle
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
import sys


from loader import dataroot
from loader import loadVoice
from CMUDict import CMUDict
from util import record
from util import writeWav
from util import RATE
from model import Voice



def main():
  if len(sys.argv) == 1:
    print 'No parameters :(. Usage: python TTS.py "Phrase to say" <userid>'
    return 1
  name = ""
  if len(sys.argv) == 2:
    print "No userid provided! Using 'DEFAULT'"
    name = 'DEFAULT'
  else:
    name = sys.argv[2]
  txt = sys.argv[1]
  
  v = loadVoice(name)
  if v is None:
    print "User " + str(name) + " does not exist. Exiting."
    return 1
    
  print "Loading CMU Dict..."
  cmu = CMUDict()
  cmu.load_dict("dict.p")
  print "Done."
  print "Rendering audio to output.wav..."
  writeWav("output.wav", v.tts(txt, cmu))
  print "Done"
  
if __name__ == "__main__":
    main()