import unittest

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
from util import CHUNK
from model import Voice

class TestModelMethods(unittest.TestCase):

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
      
      self.assertEqual(np.mean(np.abs(self.v.normalize(self.testset["frames"]))), 1799.6127134811047)
      
    def test_processPunctuation(self):
      result = self.v.processPunctuation("hel'LO worl\D. But ther/e, is no!".strip().split())
      ans = ["hello", "world", " ", "but", "there", " ", "is", "no", " "]
      self.assertEqual(result, ans)
      
      result = self.v.processPunctuation("http://www.google.com".strip().split())
      ans = ["h", "t", "t", "p", "w", "w", "w", "google", "com"]
      self.assertEqual(result, ans)
      
      result = self.v.processPunctuation("This is the best. But this is not. lulz.".strip().split())
      ans = ["this", "is", "the", "best", " ", "but", "this", "is", "not", " ", "lulz", " " ]
      self.assertEqual(result, ans)
      
    def test_volume(self):
      self.assertEqual(self.v.volume(self.testset["OW"]), 4845)
      ans = [ 5256, 9185, 4430, 3972, 10004, 4503, 4158, 10091, 4015, 4106]
      for i in range(10):
        self.assertEqual(self.v.volume(self.testset["OW"][i * 100:i * 100 + 100]), ans[i])
      
      

if __name__ == '__main__':
    unittest.main()