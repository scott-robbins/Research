from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy.io import wavfile
from threading import Thread
import numpy as np
import time
import sys
import os


if '-in' in sys.argv and len(sys.argv) >= 2:
    file_in = sys.argv[2]
    sample_rate, audio = wavfile.read(file_in)
    audio = np.array(audio)
    len_sec = audio.shape[0] / sample_rate

    f = plt.figure()
    ani = []
    state = np.array(audio[0:sample_rate,0]).reshape((200, 240))
    ani.append([plt.imshow(state, 'gray')])
    for i in range(1, int(len_sec)):
        state = np.array(audio[i*sample_rate:i*sample_rate+sample_rate,0]).reshape((200, 240))
        ani.append([plt.imshow(state,'gray')])
    a = animation.ArtistAnimation(f, ani, interval=750, blit=True)
    plt.show()