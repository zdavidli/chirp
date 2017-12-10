# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os

import tensorflow as tf
from layers import prenet, cbhg
from load_data import get_mfccs_and_phones_queue
from utils import load_vocab


class Phoneme_Classifier:
    def __init__(self, data_path, batch_size=32, mode="Train", queue=True):
        self.data_path = data_path
        self.batch_size = batch_size
        self.queue = queue
        self.mode = mode

        # Input
        self.x_mfcc, self.y_ppgs, self.y_spec, self.y_mel, self.num_batches = self.get_input()

        # Networks
        self.net_template = tf.make_template('net', self._net)
        self.ppgs, self.pred_ppg, self.logits_ppg, self.pred_spec, self.pred_mel = self.net_template()

    def __call__(self):
        return self.pred_spec

    def _net(self, hidden_units=256, dropout_rate=0.2, num_banks=16, num_highway_blocks=4, norm_type='ins', t-1.0):

        # Load vocabulary
        phn2idx, idx2phn = load_vocab()

        # Pre-net
        net = prenet(self.x_mfcc, num_units=[hidden_units, hidden_units // 2], 
                            dropout_rate=dropout_rate, is_training=self.mode)  # (N, T, E/2)

        # CBHG
        net = cbhg(net, num_banks, hidden_units // 2, num_highway_blocks, norm_type, self.mode)

        # Final linear projection
        logits = tf.layers.dense(net, len(phn2idx))  # (N, T, V)
        ppgs = tf.nn.softmax(logits / t)  # (N, T, V)
        preds = tf.to_int32(tf.arg_max(logits, dimension=-1))  # (N, T)

        return ppgs, preds, logits

    def get_input(self, n_mfcc=40, n_fft=512, n_mels = 80):
        x_mfcc = tf.placeholder(tf.float32, shape=(self.batch_size, None, n_mfcc))
        y_ppgs = tf.placeholder(tf.int32, shape=(self.batch_size, None,))
        y_spec = tf.placeholder(tf.float32, shape=(self.batch_size, None, 1+n_fft // 2))
        y_mel = tf.placeholder(tf.float32, shape=(self.batch_size, None, n_mels))

        if self.queue: 
            x_mfcc, y_ppgs, num_batches = self.get_batch_queue()
        return x_mfcc, y_ppgs, y_spec, y_mel, num_batches


    def get_batch_queue(n_mfcc=40):
        '''Loads data and put them in mini batch queues.
        mode: A string. Either `train1` | `test1` | `train2` | `test2` | `convert`.
        '''
        with tf.device('/cpu:0'):
            wav_files = glob.glob(self.data_path)
            num_batches = len(wav_files) // self.batch_size # calc total batch count
            wav_files = tf.convert_to_tensor(wav_files) # Convert to tensor
            wav_file, = tf.train.slice_input_producer([wav_files, ], shuffle=True, capacity=128) # Create Queues

            # Get inputs and target
            mfcc, ppg = get_mfccs_and_phones_queue(inputs=wav_file, dtypes=[tf.float32, tf.int32], capacity=2048, num_threads=32)

            # create batch queues
            mfcc, ppg = tf.train.batch([mfcc, ppg],
                                       shapes=[(None, n_mfcc), (None,)],
                                       num_threads=32,
                                       batch_size=self.batch_size,
                                       capacity=self.batch_size * 32,
                                       dynamic_pad=True)
            return mfcc, ppg, num_batches


    def get_batch(batch_size):
        with tf.device('/cpu:0'):
            # Load data
            wav_files = glob.glob(self.data_path)
            target_wavs = sample(wav_files, self.batch_size)

            if mode in ('train1', 'test1'):
                mfcc, ppg = map(_get_zero_padded, zip(*map(lambda w: get_mfccs_and_phones(w, hp_default.sr), target_wavs)))
                return mfcc, ppg
            else:
                mfcc, spec, mel = map(_get_zero_padded, zip(*map(
                    lambda wav_file: get_mfccs_and_spectrogram(wav_file, duration=hp_default.duration), target_wavs)))
                return mfcc, spec, mel



    def loss(self):
        istarget = tf.sign(tf.abs(tf.reduce_sum(self.x_mfcc, -1)))  # indicator: (N, T)
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.logits_ppg / hp.Train1.t, labels=self.y_ppgs)
        loss *= istarget
        loss = tf.reduce_mean(loss)
        return loss

    def acc(self):
        istarget = tf.sign(tf.abs(tf.reduce_sum(self.x_mfcc, -1)))  # indicator: (N, T)
        num_hits = tf.reduce_sum(tf.to_float(tf.equal(self.pred_ppg, self.y_ppgs)) * istarget)
        num_targets = tf.reduce_sum(istarget)
        acc = num_hits / num_targets
        return acc

    ### Static Methods
    @staticmethod
    def load(sess, mode, logdir, logdir2=None):

        def print_model_loaded(mode, logdir):
            model_name = Model.get_model_name(logdir)
            print('Model loaded. mode: {}, model_name: {}'.format(mode, model_name))

        var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'net/phoneme_classifier')
        if Model._load_variables(sess, logdir, var_list=var_list):
            print_model_loaded(mode, logdir)

    @staticmethod
    def _load_variables(sess, logdir, var_list):
        ckpt = tf.train.latest_checkpoint(logdir)
        if ckpt:
            tf.train.Saver(var_list=var_list).restore(sess, ckpt)
            return True
        else:
            return False

    @staticmethod
    def get_model_name(logdir):
        path = '{}/checkpoint'.format(logdir)
        if os.path.exists(path):
            ckpt_path = open(path, 'r').read().split('"')[1]
            _, model_name = os.path.split(ckpt_path)
        else:
            model_name = None
        return model_name

    @staticmethod
    def get_global_step(logdir):
        model_name = Model.get_model_name(logdir)
        if model_name:
            gs = int(model_name.split('_')[3])
        else:
            gs = 0
        return gs

    @staticmethod
    def all_model_names(logdir):
        import glob, os
        path = '{}/*.meta'.format(logdir)
        model_names = map(lambda f: os.path.basename(f).replace('.meta', ''), glob.glob(path))
        return model_names
