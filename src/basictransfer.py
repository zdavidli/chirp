
import numpy as np
import pickle
import os
import os.path
import librosa
import tensorflow as tf
from basictts import ttsbase
    

def testNeural():
    #ttsbase("What a wonderful world Johns Hopkins University is a top 10 university Ronny D is just the swellest person This is a completely different text that hopefully sounds unique from the other one", "static/diff.", 0.8)

    test = 0

    # Reads wav file and produces spectrum
    # Fourier phases are ignored
    N_FFT = 2048
    def read_audio_spectum(filename):
        x, fs = librosa.load(filename)
        S = librosa.stft(x, N_FFT)
        p = np.angle(S)
        
        S = np.log1p(np.abs(S[:,:430]))    
        return S, fs

    CONTENT_FILENAME = "static/diff_12s.wav"#"static/diff_10s.wav"
    STYLE_FILENAME = "static/traindata/gary/0_10s.wav"

    a_content, fs = read_audio_spectum(CONTENT_FILENAME)
    a_style, fs = read_audio_spectum(STYLE_FILENAME)

    N_SAMPLES = a_content.shape[1]
    N_CHANNELS = a_content.shape[0]
    a_style = a_style[:N_CHANNELS, :N_SAMPLES]

    ######################################################

    #plt.figure(figsize=(10, 5))
    #plt.subplot(1, 2, 1)
    #plt.title('Content')
    #plt.imshow(a_content[:400,:])
    #plt.subplot(1, 2, 2)
    #plt.title('Style')
    #plt.imshow(a_style[:400,:])
    #plt.show()

    ######################################################

    N_FILTERS = 4096

    a_content_tf = np.ascontiguousarray(a_content.T[None,None,:,:])
    a_style_tf = np.ascontiguousarray(a_style.T[None,None,:,:])

    # filter shape is "[filter_height, filter_width, in_channels, out_channels]"
    std = np.sqrt(2) * np.sqrt(2.0 / ((N_CHANNELS + N_FILTERS) * 11))
    kernel = np.random.randn(1, 11, N_CHANNELS, N_FILTERS)*std
        
    g = tf.Graph()
    with g.as_default(), g.device('/cpu:0'), tf.Session() as sess:
        # data shape is "[batch, in_height, in_width, in_channels]",
        x = tf.placeholder('float32', [1,1,N_SAMPLES,N_CHANNELS], name="x")

        kernel_tf = tf.constant(kernel, name="kernel", dtype='float32')
        conv = tf.nn.conv2d(
            x,
            kernel_tf,
            strides=[1, 1, 1, 1],
            padding="VALID",
            name="conv")
        
        net = tf.nn.relu(conv)

        content_features = net.eval(feed_dict={x: a_content_tf})
        style_features = net.eval(feed_dict={x: a_style_tf})
        
        features = np.reshape(style_features, (-1, N_FILTERS))
        style_gram = np.matmul(features.T, features) / N_SAMPLES

    ######################################################
    from sys import stderr
    print("test")
    ALPHA= 1.2e-2
    learning_rate= 1e-3
    iterations = 100

    result = None
    with tf.Graph().as_default():

        # Build graph with variable input
        # x = tf.Variable(np.zeros([1,1,N_SAMPLES,N_CHANNELS], dtype=np.float32), name="x")
        x = tf.Variable(np.random.randn(1,1,N_SAMPLES,N_CHANNELS).astype(np.float32)*1e-3, name="x")

        kernel_tf = tf.constant(kernel, name="kernel", dtype='float32')
        conv = tf.nn.conv2d(
            x,
            kernel_tf,
            strides=[1, 1, 1, 1],
            padding="VALID",
            name="conv")
        
        
        net = tf.nn.relu(conv)

        content_loss = ALPHA * 2 * tf.nn.l2_loss(
                net - content_features)

        style_loss = 0

        _, height, width, number = map(lambda i: i.value, net.get_shape())

        size = height * width * number
        feats = tf.reshape(net, (-1, number))
        gram = tf.matmul(tf.transpose(feats), feats)  / N_SAMPLES
        style_loss = 2 * tf.nn.l2_loss(gram - style_gram)

         # Overall loss
        loss = content_loss + style_loss

        opt = tf.contrib.opt.ScipyOptimizerInterface(
              loss, method='L-BFGS-B', options={'maxiter': 300})
            
        # Optimization
        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
           
            print('Started optimization.')
            opt.minimize(sess)
            #saver = tf.train.Saver()
            #save_path = saver.save(sess, "static/models/gary.model")
        
            print('Final loss:' + str(loss.eval()))
            result = x.eval()

    #save_path = saver.save(sess, "static/models/gary.model")


    ######################################################

    a = np.zeros_like(a_content)
    a[:N_CHANNELS,:] = np.exp(result[0,0].T) - 1

    # This code is supposed to do phase reconstruction
    p = 2 * np.pi * np.random.random_sample(a.shape) - np.pi
    for i in range(500):
        S = a * np.exp(1j*p)
        x = librosa.istft(S)
        p = np.angle(librosa.stft(x, N_FFT))

    OUTPUT_FILENAME = 'static/out.wav'
    librosa.output.write_wav(OUTPUT_FILENAME, x, fs)

def pitchFromData(user_id):
    filebase = "static/traindata/" + user_id+ "/"
    counter = 0
    totPitch = 0
    files = 0
    while (True):
        filename = filebase + str(counter) + ".wav"
        if (os.path.isfile(filename) == False):
            break
        y, sr = librosa.load(filename, sr=40000)
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, fmin=75, fmax=1600)

        np.set_printoptions(threshold=np.nan)
        s = 0
        i = 0
        for t in range(0, pitches.shape[1], 3):
            # print magnitudes[:,t].mean()
            if (magnitudes[:,t].mean() > 0.03):
                s += detect_pitch(pitches, magnitudes, t)
                i += 1
        if (i != 0):
            totPitch += s / i
            files += 1
        counter += 1
    pitch = totPitch / files
    pickle.dump(pitch, open("static/pitches/" + user_id, "wb"))
    return pitch



def detect_pitch(pitches, magnitudes, t):
    index = magnitudes[:, t].argmax()
    pitch = pitches[index, t]

    return pitch


if __name__ == "__main__":
    testNeural()