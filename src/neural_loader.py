#import pyaudio
import wave
import pickle
import librosa #For saving files
from os import path
from os import walk
from os import listdir
import os
import csv

from model import Model

class VoiceDB:

  def __init__(self):
    self.models = dict()
  # Returns the model with fallback.
  def getModel(self, id):
    if (str(id) not in self.models):
      print("Loading model from disk: " + str(id))
      self.models[str(id)] = self.loadModel(str(id))
      print("Model loaded.")
    return self.models[str(id)]

  # Load model from disk
  def loadModel(self, id):
    m = Model(str(id))
    return m

  # Discard loaded model and reload if retrained
  def reloadModel(self, id):
    self.models[str(id)] = self.loadModel(str(id))