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

class Renderer:
  
  def __init__(self, id):
    pass
    
  @staticmethod
  def serialize(input):
    return np.concatenate(input)
  @staticmethod
  def renderWord(voice, pron):
    out = voice.phonemes[pron[0][0]]
    for i in range(1,len(pron)):
      out = Renderer.concat(out, voice.phonemes[pron[i][0]], RATE * 0.1)
      #print len(out)
    return out
  @staticmethod
  def concat(v1, v2, i=0):
    i = int(min(i, len(v1)))
    v1, v2 = v1.astype(np.int32), v2.astype(np.int32)
    left = v1[:len(v1) - i]
    right = []
    m1 = []
    m2 = []
    if i >= len(v2):
      right = v1[len(v1) - i:len(v1) - i + len(v2)]
      m1 = v1[len(v1) - i:len(v1) - i + len(v2)]
      m2 = v2
    else:
      right = v2[i:]
      m1 = v1[len(v1) - i:]
      m2 = v2[:i]
    m1 = m1[:len(m2)] + m2
    m1[m1>32767] = 32767
    m1[m1<-32767] = -32767
    return np.append(np.append(left, m1), right).astype(np.int16)
    return combined.astype(np.int16)
  @staticmethod
  def normalize(audio):
    mean = np.mean(np.abs(audio))
    ratio = mean / 2000.0
    return (audio / ratio).astype(np.int16)
      
  # Cut out the initial silence
  @staticmethod
  def trimFront(audio):
    i = 0
    sample = int(RATE / 100)
    while (Renderer.volume(audio[i:i+sample:2]) < 1500):
      i += sample * 4
    return audio[i:]
  @staticmethod
  def trimBack(audio):
    i = len(audio) - 1
    sample = int(RATE / 100)
    while (Renderer.volume(audio[i-sample:i:2]) < 1500):
      i -= sample * 4
    return audio[:i]
  @staticmethod
  def volume(audio):
    return np.sum(abs(audio)) / len(audio)
  
  # Text to speech
  @staticmethod
  def tts(voice,txt,dict,delay=0.2):
    wordStrs = Renderer.processPunctuation(txt.strip().split())
    out = np.zeros(1).astype(np.int16)
    for word in wordStrs:
      if word == ' ':
        out = np.concatenate((out, np.zeros((int(RATE * delay))).astype(np.int16), np.zeros((int(RATE * delay))).astype(np.int16)))
      #TODO do not always take the first translation
      else:
        conv = dict.get_phonemes_from_text(word)[0]
        if conv is not None:
          ######TEMP#######
          if (conv[1] == ("AH",0)):
            conv[1] = ("EH",0)
          ################
          out = np.concatenate((out, Renderer.renderWord(voice, conv), np.zeros((int(RATE * delay))).astype(np.int16)))
    return out
  @staticmethod
  def processPunctuation(wordStrs):
    words = []
    for word in wordStrs:
      word = word.lower()
      word = word.replace(",", ".")
      word = word.replace(";", ".")
      word = word.replace(":", ".")
      word = word.replace("/", "")
      word = word.replace("\\", "")
      word = word.replace("\"", "")
      word = word.replace("\'", "")
      
      
      #TEMP Replace ? and ! with .
      word = word.replace("?", ".")
      word = word.replace("!", ".")
      word = word.replace("http", ".h.t.t.p.")
      word = word.replace("www", ".w.w.w.")
      word = word.replace("http", ".h.t.t.p.s.")
      
      word = word.replace("..", ".")
      
      wordsplit = word.split(".")
      while '' in wordsplit:
        wordsplit.remove('')
      if len(word) > 0 and word[-1] == ".":
        wordsplit.append(" ")
      words += wordsplit
    return words