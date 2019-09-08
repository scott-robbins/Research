import matplotlib.pyplot as plt
import scipy.signal as signal
from threading import Thread
import scipy.ndimage as ndi
import numpy as np
import librosa
import os


def play_wav(file_name, volume):
    vol = {}
    i = 0
    for ii in np.linspace(0, 65535, 10):
        vol[i] = ii
        i += 1
    try:
        cmd = 'paplay --volume=%d %s' % (file_name. vol[volume])
    except KeyError:
        print '\033[31m\033[1m\033[3m** ERROR: Volume Must be Between [0-10]! **\033[0m'
    print cmd
    os.system(cmd)


def rec(name):
    cmd = 'sox -t alsa default %s &' % name
    os.system(cmd)


def start_recording(file_out):
    record = Thread(target=rec, args=(file_out,))
    record.start()
    record.join()
    return record


def stop_recording():
    cmd = "ps aux | grep 'sox -t' | cut -b 11-16 | while read n; do echo $n; kill -9 $n; done"
    os.system(cmd)


def MP3toWAV(file_path):
    file_out = file_path.split('.mp3')[0].split('/')[len(file_path.split('/'))-1]+'.wav'
    print 'Converting %s to %s' % (file_path,file_out)
    cmd = 'ffmpeg -loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s' % (file_path, file_out)
    os.system(cmd)


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


def profile_signal(data_in, binning):
    minima = binning['min']
    maxima = binning['max']
    n_bins = binning['bins']
    bins = np.linspace(minima, maxima, n_bins)
    db = bins[1]-bins[0]

    hist = {}
    for pt in np.array(data_in).flatten():
        for b in bins:
            ptl = pt-db
            pth = pt+db
            if ptl<=int(b)<=pth:
                hist[int(b)] += 1


test = '../AST/inputs/me_30s.mp3'
into = 'me_30s.wav'
MP3toWAV(test)
Sound, fqs = read_audio_spectum(into)
# hist = ndi.gaussian_laplace(Sound,sigma=0.1)
hist = profile_signal(ndi.gaussian_laplace(Sound,sigma=0.1), {'min':20,'max':5000,'bins':500})


f, ax = plt.subplots(1,2, figsize=(5,5))
ax[0].imshow(Sound[:, :])
ax[1].plot(hist.keys(), hist.values())
plt.show()
os.system('rm %s' % into)