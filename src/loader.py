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

dataroot = "voices/"

# Loads the voice for the specified user.
# returns None if the user has no voice model.
def loadVoice(userid):
  try:
    v = pickle.load(open(dataroot + str(userid) + ".dat", 'r'))
    return v
  except:
    return None

  
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

class VoiceDB:

  def __init__(self):
    self.models = dict()

  def getModel(self, id):
    if (str(id) not in self.models):
      print("Loading model from disk: " + str(id))
      self.models[str(id)] = self.loadModel(str(id))
      print("Model loaded.")
    return self.models[str(id)]

  def loadModel(self, id):
    m = Model(str(id))
    return m

  def reloadModel(self, id):
    self.models[str(id)] = self.loadModel(str(id))



class VoiceIO():
    """
    A class to handle loading, saving, and deleting of voice data
    """
    def __init__(self):
        base = "static"
        self.render_dir = os.path.join(base, "audio")
        self.pitch_dir = os.path.join(base, "pitches")
        self.train_dir = os.path.join(base, "traindata")
    
    def deleteTrainData(self, userId):
        """
        Input: userId, a string
        
        Returns: True if all training data was succesfully deleted
                 False otherwise
        """
        try:
            root = os.path.join(self.train_dir, userId)
            counter = 0
            name = str(counter) + '.wav'
            filename = os.path.join(root,name)
            while os.path.isfile(filename):
                os.remove(filename)
                counter += 1
                filename = os.path.join(root, str(counter)+'.wav')
            if (os.path.isfile(os.path.join(self.pitch_dir, userId))):
                os.remove(os.path.join(self.pitch_dir,userId))
            return True
        except Exception as e:
            print(e)
            return False

    def getNextTrainFile(self, userId):
        """
        Input: userId, a string

        Returns: Filename, a string representing the name of the file 
                 where the next train file for a user should be saved
        """
        root = os.path.join(self.train_dir, userId)
        counter = 0
        filename = os.path.join(root, str(counter)+'.wav')
        while os.path.isfile(filename):
            counter += 1
            filename = os.path.join(root, str(counter)+'.wav')
        if not os.path.exists(root):
            os.makedirs(root)
        return filename
            
    def saveWav(self,userId, x, sample_rate, filename = None):
        """
        Saves a wav file for the specified user
        Input: userId, a string
               x, wav data that can be saved with librosa
               sample_rate, the sample rate of the audio data
               filename, the location to save the file, defaults to next train file for theuser
        Return: filename, the file the data was saved at
        """
        if filename is None:
            filename = self.getNextTrainFile(userId)
        librosa.output.write_wav(filename, x, sample_rate)
        return filename
    
    def loadWav(self, fileName):
        """
        Input: fileName, a string
        Return: x, audio data
                fs, sample rate for the audio data
        """
        return librosa.load(fileName)


    def numSamples(self, userId):
        """
        Input: userId, a string
        Return: the number of training samples that exist for this user
        """
        root = os.path.join(self.train_dir,userId)
        counter = 0
        filename = os.path.join(self.train_dir, str(counter)+'.wav')
        while os.path.isfile(filename):
            counter += 1
            filename = os.path.join(self.train_dir, str(counter)+'.wav')
        return counter
        


