import unittest
import pyaudio
import wave
import cPickle as pickle
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
import copy

from loader import loadVoice
from loader import dataroot
from CMUDict import CMUDict
from CMUDict import ALL_PHONEMES
from util import record
from util import writeWav
from util import RATE
from util import CHUNK
from model import Voice
from renderer import Renderer

class TestModel(unittest.TestCase):

    def setUp(self):
      self.v = Voice("testname")
      self.testset = pickle.load(open("testset.dat", 'rb'))
      
    def tearDown(self):
      pass

      
    def test_modelInit(self):
      self.assertEqual(self.v.userid, "testname")
      self.assertEqual(len(self.v.phonemes.keys()), 0)
      
    def test_modelAddPhoneme(self):
      self.assertEqual(self.v.userid, "testname")
      self.assertEqual(len(self.v.phonemes.keys()), 0)
      
      self.v.addPhoneme("t", self.testset["frames"])
      self.assertTrue(len(self.v.phonemes["t"]) < 88064 / 2)
      
      self.assertEqual(len(self.v.phonemes.keys()), 1)
      
    def test_modelNorm(self):
      self.assertEqual(self.v.userid, "testname")
      self.assertEqual(len(self.v.phonemes.keys()), 0)
      
      self.assertEqual(np.mean(np.abs(Renderer.normalize(self.testset["frames"]))), 1578.1323582848838)
      
    def test_processPunctuation(self):
      result = Renderer.processPunctuation("hel'LO worl\D. But ther/e, is no!".strip().split())
      ans = ["hello", "world", " ", "but", "there", " ", "is", "no", " "]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("http://www.google.com".strip().split())
      ans = ["h", "t", "t", "p", "w", "w", "w", "google", "com"]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("This is the best. But this is not. lulz.".strip().split())
      ans = ["this", "is", "the", "best", " ", "but", "this", "is", "not", " ", "lulz", " " ]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("...".strip().split())
      ans = [ " " ]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("bruh...".strip().split())
      ans = [ "bruh", " " ]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("KaPPa PRIDE!".strip().split())
      ans = [ "kappa", "pride", " " ]
      self.assertEqual(result, ans)
      
      result = Renderer.processPunctuation("".strip().split())
      ans = [ ]
      self.assertEqual(result, ans)
      
    def test_volume(self):
      self.assertEqual(Renderer.volume(self.testset["OW"]), 4845)
      ans = [ 5256, 9185, 4430, 3972, 10004, 4503, 4158, 10091, 4015, 4106]
      for i in range(10):
        self.assertEqual(Renderer.volume(self.testset["OW"][i * 100:i * 100 + 100]), ans[i])
        
    def test_missingPhonemes(self):
      result = self.v.missingPhonemes()
      remainingPhonemes = copy.copy(ALL_PHONEMES)
      self.assertEqual(result, remainingPhonemes)
      self.assertFalse(self.v.isFullyTrained())
      
      input = np.random.rand(43, 1024) * 22000 - 128
      self.v.addPhoneme("AA", input)
      result = self.v.missingPhonemes()
      remainingPhonemes.remove("AA")
      self.assertEqual(result, remainingPhonemes)
      
      
      for p in copy.copy(remainingPhonemes):
        self.v.addPhoneme(p, input)
        result = self.v.missingPhonemes()
        remainingPhonemes.remove(p)
        self.assertEqual(result, remainingPhonemes)
      self.assertTrue(self.v.isFullyTrained())
      
    def test_trainedPhonemes(self):
      result = self.v.trainedPhonemes()
      remainingPhonemes = set()
      self.assertEqual(result, remainingPhonemes)
      self.assertFalse(self.v.isFullyTrained())
      
      input = np.random.rand(43, 1024) * 22000 - 128
      self.v.addPhoneme("AA", input)
      result = self.v.trainedPhonemes()
      remainingPhonemes.add("AA")
      self.assertEqual(result, remainingPhonemes)
      
      
      for p in copy.copy(remainingPhonemes):
        self.v.addPhoneme(p, input)
        result = self.v.trainedPhonemes()
        remainingPhonemes.add(p)
        self.assertEqual(result, remainingPhonemes)
      self.assertFalse(self.v.isFullyTrained())

if __name__ == '__main__':
    unittest.main()