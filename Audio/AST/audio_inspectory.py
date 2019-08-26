import matplotlib.pyplot as plt
import Tkinter as Tk
import numpy as np
import librosa
import time
import sys
import os


def read_audio_spectum(filename):
    """
    Reads wav file and produces spectrum
    Fourier phases are ignored
    :param filename:
    :return stfft, file:
    """
    N_FFT = 2048
    x, fs = librosa.load(filename)
    S = librosa.stft(x, N_FFT)
    p = np.angle(S)

    S = np.log1p(np.abs(S[:, :]))
    return S, fs


N_FFT = 2048
tic = time.time()

audio_file_name = sys.argv[1]
audio_file, fs = read_audio_spectum(audio_file_name)
print audio_file.shape
n_channels = audio_file.shape[0]
n_samples = audio_file.shape[1]

print '~ %s Loaded ~' % audio_file_name
print '  * %d Channels ' % n_channels
print '  * %d Samples' % n_samples

audio_content = audio_file[:n_channels, :n_samples]
plt.imshow(audio_content)
plt.show()


