import codecs
import csv
import os
import re

from hyperparams import Hyperparams as hp
import numpy as np


def load_vocab():
    vocab = "EG abcdefghijklmnopqrstuvwxyz'" # E: Empty. ignore G
    char2idx = {char:idx for idx, char in enumerate(vocab)}
    idx2char = {idx:char for idx, char in enumerate(vocab)}
    return char2idx, idx2char    

def create_train_data():
    # Load vocabulary
    char2idx, idx2char = load_vocab() 
      
    texts, sound_files = [], []
    i = 0
    reader = csv.reader(codecs.open(hp.text_file, 'rb', 'utf-8'))
    for row in reader:
        sound_fname, text, duration = row
        #print text, len(text)
        sound_file = hp.sound_fpath + "/" + sound_fname + ".wav"
        text = re.sub(r"[^ a-z']", "", text.strip().lower())
         
        if hp.min_len <= len(text) <= hp.max_len:
            #print "um"
            texts.append(np.array([char2idx[char] for char in text], np.int32).tostring())
            sound_files.append(sound_file)
        i += 1
        if i > 100:
            break
             
    return texts, sound_files
     
def load_train_data():
    """We train on the whole data but the last num_samples."""
    texts, sound_files = create_train_data()
    if hp.sanity_check: # We use a single mini-batch for training to overfit it.
        texts, sound_files = texts[:hp.batch_size]*1000, sound_files[:hp.batch_size]*1000
    else:
        texts, sound_files = texts[:-hp.num_samples], sound_files[:-hp.num_samples]
    return texts, sound_files
 
def load_eval_data():
    """We evaluate on the last num_samples."""
    texts, _ = create_train_data()
    if hp.sanity_check: # We generate samples for the same texts as the ones we've used for training.
        texts = texts[:hp.batch_size]
    else:
        texts = texts[-hp.num_samples:]
    
    X = np.zeros(shape=[len(texts), hp.max_len], dtype=np.int32)
    for i, text in enumerate(texts):
        _text = np.fromstring(text, np.int32) # byte to int 
        X[i, :len(_text)] = _text
    
    return X

def process_text(text):
    assert 10 <= len(text) <= 100
    char2idx, idx2char = load_vocab() 
    text = re.sub(r"[^ a-z']", "", text.strip().lower())
    return np.fromstring(np.array([char2idx[char] for char in text], np.int32).tostring(), np.int32)

def send_texts(texts=["Hello World", "I am a complete degenerate", "Johns Hopkins is a top ten univeristy"]):
    X = np.zeros(shape=[len(texts), 100], dtype=np.int32)
    for i, text in enumerate(texts):
        text = process_text(text)
        X[i, :len(text)] = text
        
    return X