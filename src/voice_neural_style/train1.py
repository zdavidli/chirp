# -*- coding: utf-8 -*-
# /usr/bin/python2

from __future__ import print_function

from hparams import logdir_path
from tqdm import tqdm

from layers import *
from Phoneme_Classifier import Phoneme_Classifier
import eval1
from data_load import get_batch
import argparse


def train(logdir='logdir/phoneme_classifier', data_path='datasets/TIMIT/TRAIN/*/*/*.WAV', num_epochs=1000, lr=0.0003, queue=True):
    model = Phoneme_Classifier(data_path, queue)

    ### 1. Initializing operations
    loss_op = model.loss() # loss operation
    acc_op = model.acc() # accuracy operation
    global_step = tf.Variable(0, name='global_step', trainable=False) # Training Scheme

    optimizer = tf.train.AdamOptimizer(learning_rate=lr)
    with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
        var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'net/phoneme_classifier')
        train_op = optimizer.minimize(loss_op, global_step=global_step, var_list=var_list)

    tf.summary.scalar('phoneme_classifier/train/loss', loss_op)
    tf.summary.scalar('phoneme_classifier/train/acc', acc_op)
    summ_op = tf.summary.merge_all()

    # Training
    session_conf = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
    with tf.Session(config=session_conf) as sess:
        # Load trained model
        sess.run(tf.global_variables_initializer())

        writer = tf.summary.FileWriter(logdir, sess.graph)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        for epoch in range(1, num_epochs + 1):
            for step in tqdm(range(model.num_batches), total=model.num_batches, ncols=70, leave=False, unit='b'):
                if queue:
                    sess.run(train_op)
                else:
                    mfcc, ppg = get_batch(model.mode, model.batch_size)
                    sess.run(train_op, feed_dict={model.x_mfcc: mfcc, model.y_ppgs: ppg})

            # Write checkpoint files at every epoch
            summ, gs = sess.run([summ_op, global_step])

            if epoch % hp.Train1.save_per_epoch == 0:
                tf.train.Saver().save(sess, '{}/epoch_{}_step_{}'.format(logdir, epoch, gs))

            # Write eval accuracy at every epoch
            with tf.Graph().as_default():
                eval1.eval(logdir=logdir, queue=False)

            writer.add_summary(summ, global_step=gs)

        writer.close()
        coord.request_stop()
        coord.join(threads)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', default="default", type=str, help='experiment case name')
    arguments = parser.parse_args()
    return arguments

if __name__ == '__main__':
    args = get_arguments()
    case = args.case
    logdir = '{}/{}/train1'.format(logdir_path, case)
    train(logdir=logdir)
    print("Done")