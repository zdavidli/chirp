import pyaudio
import wave
import pickle
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
import copy

# Custom Code
from CMUDict import CMUDict
from CMUDict import ALL_PHONEMES
from renderer import Renderer



class Voice:
  
  def __init__(self, id):
    self.phonemes = dict()
    self.userid = id
    #if self.userid+"_PhonemeBank" not in os.listdir(os.path.abspath("VoiceData/")):
      #self.generatePhonemeDict()
    #  pass
    #else if len(os.listdir(os.path.abspath("VoiceData/"+self.userid+"_PhonemeBank"))) < 44:
    #  self.generatePhonemeDict()
    
  def __hash__(self):
    return self.userid
  
  def generatePhonemeDict(self):
      pronounce_dict = {}
      with open("cmudict.pronounciations", "r") as infile:
          for line in infile.readlines():
              line = line.split("\t")
              line[2] = line[2].rstrip("\n")
              pronounce_dict[line[0]] = line[1:]

      for phoneme in sorted(cmudict.get_phonemes()):
        print("Pronounce " + phoneme + " like " + phoneme + " in " \
          + pronounce_dict[phoneme][0] + " (Spelled " \
          + pronounce_dict[phoneme][1] + "). ENTER when done.")
          
        self.addPhoneme(phoneme, record(3))
        _listener = raw_input("Hit ENTER to continue.")
        writeWav("id"+phoneme+".wav", self.phonemes[phoneme])

  def addPhoneme(self, key, audio):
    self.phonemes[key] = Renderer.normalize(Renderer.trimBack(Renderer.trimFront(Renderer.serialize(audio))))
    
  def getPhoneme(self, key):
    return self.phonemes[key]
    
  def renderWord(self, pron):
    return Renderer.renderWord(self, pron)
    
  def setId(self, id):
    self.userid = id
    
  def save(self, root=None):
    if root is None:
      root = dataroot
    pickle.dump(self,open(root + str(self.userid) + ".dat", 'wb'))
  
  # Text to speech
  def tts(self,txt,dict,delay=0.1):
    return Renderer.tts(self, txt, dict, delay)
  
  # Returns a set of all remaining phonemes that need to be trained
  def missingPhonemes(self):
    remainingPhonemes = copy.copy(ALL_PHONEMES)
    for k in self.phonemes.keys():
      remainingPhonemes.remove(k)
    return remainingPhonemes
  
  # Returns a set of all phonemes that have been trained
  def trainedPhonemes(self):
    return set(self.phonemes.keys())
  
  # Returns True if the phoneme set is complete (has all nessecary phonemes for english)
  def isFullyTrained(self):
    if len(self.missingPhonemes()) == 0:
      return True
    return False
