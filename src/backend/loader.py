import pyaudio
import wave
import cPickle as pickle
from os import path
from os import walk
from os import listdir
import os
import csv

dataroot = "voices/"

def loadVoice(userid):
  return pickle.load(open(dataroot + str(userid) + ".dat", 'rb'))

  
# Returns a dict of all voices stored in /voices/
def loadAllVoices():
  voices = dict()
  rootdir = './'
  for subdir, dirs, files in os.walk(rootdir + dataroot):
    for file in files:
      fname = path.join(subdir, file).replace('\\','/')
      #print labelpath
      if '.dat' in fname:
        try:
          v = pickle.load(open(fname, 'rb'))
          voices[v] = v
        except:
          pass
  return voices