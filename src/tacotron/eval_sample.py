import codecs
import copy
import os

import librosa
from scipy.io.wavfile import write

from hyperparams import Hyperparams as hp
import numpy as np
from prepro import *
import tensorflow as tf
from train import Graph
from utils import *

X = load_eval_data() # textsa
print X