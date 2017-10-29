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
      
      
      
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()