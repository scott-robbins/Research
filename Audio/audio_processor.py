from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy.io import wavfile
from threading import Thread
import scipy.ndimage as ndi
import numpy as np
import time
import sys
import os

tic = time.time()

w = 210
h = 210

k0 = [[1,1,1],[1,0,1],[1,1,1]]


def play(song):
    print 'Playing %s' % song
    os.system('sleep 4; paplay %s &' % song)


def sigmoid(arr):
    dataout = []
    for element in arr.flatten():
        dataout.append((1/(1+np.power(np.e,-1*element)))*2)
    return dataout


def automatize(sec, state,W,H):

    if len(state.shape) > 1:
        frame = np.array(state).flatten()
        world = ndi.convolve(state, k0).flatten()
    else:
        state = np.array(state).reshape((W, H))
        world = ndi.convolve(state, k0).flatten()
        frame = np.array(state).astype(np.float).flatten()
    ii = 0
    for cell in world:
        if cell >= 6 and frame[ii] <= 0:
            frame[ii] += 1
        if cell % 6 == 0 and frame[ii] >= 1:
            frame[ii] -= 1
        if cell % 2 and frame[ii] == []:
            frame[ii] = 1
        ii += 1

    return np.array(frame.reshape(state.shape))


if '-in' in sys.argv and len(sys.argv) >= 2:
    file_in = sys.argv[2]
    sample_rate, audio = wavfile.read(file_in)
    audio = np.array(audio)
    len_sec = audio.shape[0] / sample_rate
    sound = Thread(target=play, args=(file_in,))
    if sample_rate == 48000:
        w = 200
        h = 240
    f = plt.figure()
    ani = []
    for i in range(0, int(len_sec)):
        arr = np.fft.fft(np.array(audio[i*sample_rate:i*sample_rate+sample_rate,0]), axis=0)
        state = np.array(sigmoid(arr)).astype(np.float).reshape((w, h))
        maxima = state.max()
        ani.append([plt.imshow(state)])
        ''' DO VISUALIZER MODS HERE '''
        for j in range(2):
            state = automatize(i, np.array(state),w,h)
            ani.append([plt.imshow(np.array(state))])
    sound.start()
    sound.join()
    a = animation.ArtistAnimation(f, ani, interval=250, blit=True, repeat_delay=900)
    print '\033[1m\033[31mSHOWING VISUALS [%ss Elapsed]\033[0m' % str(time.time()-tic)
    plt.show()
