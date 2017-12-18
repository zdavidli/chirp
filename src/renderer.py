import pyaudio
import wave
import pickle
import struct
import numpy as np
import scipy.io.wavfile as wavfile
import os
from CMUDict import CMUDict

trimThreshold = 1100

phonemeVolumeScale = dict()
phonemeVolumeScale['IY'] = 1.0    # ['Eat', 'fEEt']
phonemeVolumeScale['W'] =  1.2    #['We', 'Wand']
phonemeVolumeScale['DH'] = 1.2    # ['THee', 'THat']
phonemeVolumeScale['Y'] =  1.1    #['Yes', 'Yield']
phonemeVolumeScale['HH'] = 1.25    # ['He', 'Head']
phonemeVolumeScale['CH'] = 1.0    # ['CHeese', 'watCH']
phonemeVolumeScale['JH'] = 1.0    # ['Jump', 'Jack']
phonemeVolumeScale['ZH'] = 1.1    # ['sieZUre', 'Genre']
phonemeVolumeScale['EH'] = 1.0    # ['hEllo', 'Eddie']
phonemeVolumeScale['NG'] = 1.25    # ['piNG', 'haNG']
phonemeVolumeScale['TH'] = 1.1    # ['THree', 'wiTH']
phonemeVolumeScale['AA'] = 1.15    # ['Awesome', 'Odd']
phonemeVolumeScale['B'] =  1.2    #['Bat', 'haBitat']
phonemeVolumeScale['AE'] = 1.0    # ['At', 'hAt']
phonemeVolumeScale['D'] =  1.1    #['Day', 'haD']
phonemeVolumeScale['G'] =  1.2    #['Green', 'raG']
phonemeVolumeScale['F'] =  1.05    #['Fee', 'halF']
phonemeVolumeScale['AH'] = 1.2    # ['hUt', 'bUt']
phonemeVolumeScale['K'] =  1.1    #['Key', 'hacK']
phonemeVolumeScale['M'] =  1.25    #['Me', 'haM']
phonemeVolumeScale['L'] =  1.3    #['Lee', 'beLL']
phonemeVolumeScale['AO'] = 1.2    # ['bOUght', 'OUght']
phonemeVolumeScale['N'] =  1.3    #['Need', 'haNd']
phonemeVolumeScale['IH'] = 1.0    # ['It', 'hId']
phonemeVolumeScale['S'] =  1.0    #['Sea', 'hiSS']
phonemeVolumeScale['R'] =  1.3    #['Read', 'Ramble']
phonemeVolumeScale['EY'] = 1.0    # ['Ate', 'hAY']
phonemeVolumeScale['T'] =  1.15    #['Tea', 'haT']
phonemeVolumeScale['AW'] = 1.1    # ['cOW', 'mOUth']
phonemeVolumeScale['V'] =  1.3    #['Vision', 'haVE']
phonemeVolumeScale['AY'] = 1.1    # ['rIde', 'I']
phonemeVolumeScale['Z'] =  1.1   #['Zebra', 'haS']
phonemeVolumeScale['ER'] = 1.1    # ['hURt', 'bURgER']
phonemeVolumeScale['P'] =  1.2    #['Pen', 'hiP']
phonemeVolumeScale['UW'] = 1.2    # ['shOE', 'bOO']
phonemeVolumeScale['SH'] = 1.0    # ['SHe', 'slaSH']
phonemeVolumeScale['UH'] = 1.2    # ['hUg', 'rUg']
phonemeVolumeScale['OY'] = 1.1    # ['tOY', 'bOY']
phonemeVolumeScale['OW'] = 1.2    # ['bOAt', 'OAt']



class Renderer:
  
  def __init__(self, id):
    pass
    
  @staticmethod
  def serialize(input):
    return np.concatenate(input)
  @staticmethod
  def renderWord(voice, pron):
    gap = 0.12
    overallScale = 0.75
    out = Renderer.rampEdges(voice.phonemes[pron[0][0]])# * phonemeVolumeScale[pron[0][0]] * overallScale)
    if len(pron) > 5:
      gap *= 1.4
    for i in range(1,len(pron)):# * phonemeVolumeScale[pron[i][0]] * overallScale
      out = Renderer.concat(out, Renderer.rampEdges(voice.phonemes[pron[i][0]]), min(RATE * gap, len(voice.phonemes[pron[i][0]])))
    return out
    
  @staticmethod
  def rampEdges(audio):
    edge = int(len(audio) * 0.2);
    for i in range(edge):
      audio[i] *= i / edge
      audio[len(audio) - i - 1] *= i / edge
    return audio
  
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
    ratio = mean / 1700.0
    return (audio / ratio).astype(np.int16)
      
  # Cut out the initial silence
  @staticmethod
  def trimFront(audio):
    i = 0
    sample = int(RATE / 100)
    audioNorm = Renderer.normalize(audio)
    while (Renderer.volume(audioNorm[i:i+sample:2]) < trimThreshold) and len(audio) - i > sample * 9:
      i += sample * 4
    return audio[max(i,i - sample * 4):]
  @staticmethod
  def trimBack(audio):
    i = len(audio) - 1
    sample = int(RATE / 100)
    audioNorm = Renderer.normalize(audio)
    while (Renderer.volume(audioNorm[i-sample:i:2]) < trimThreshold) and i > sample * 9:
      i -= sample * 4
    return audio[:min(i,i + sample * 4)]
  @staticmethod
  def volume(audio):
    return np.sum(abs(audio)) / len(audio)
  
  # Text to speech
  @staticmethod
  def tts(voice,txt,dict,delay):
    wordStrs = Renderer.processPunctuation(txt.strip().split())
    out = np.zeros(1).astype(np.int16)
    for word in wordStrs:
      if word == ' ':
        out = np.concatenate((out, np.zeros((int(RATE * delay))).astype(np.int16), np.zeros((int(RATE * delay))).astype(np.int16)))
      #TODO do not always take the first translation
      else:
        conv = dict.get_phonemes_from_text(word)[0]
        if conv is not None:
          #######TEMP#######
          #if (conv[1] == ("AH",0)):
          #  conv[1] = ("EH",0)
          #################
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