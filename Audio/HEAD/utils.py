import numpy as np
import os


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def process_song(audio_data, name):
    sample_rate = audio_data[0]
    raw_audio = audio_data[1]
    len_sec = raw_audio.shape[0]/float(sample_rate)
    print '%s: %d ==> %f' % (name, raw_audio.shape[0], len_sec)
    FRAMES = []
    L = np.array(raw_audio[:, 0])
    R = np.array(raw_audio[:, 1])
    for i in range(int(len_sec)):
        if i>=1:
            x1 = (i-1)*sample_rate
            x2 = i*sample_rate
            frameL = L[x1:x2].mean() + L[x1:x2].std() + np.mean(np.fft.fft(raw_audio[x1:x2,0]))/sample_rate
            frameR = R[x1:x2].mean() + R[x1:x2].std() + np.mean(np.fft.fft(raw_audio[x1:x2,1]))/sample_rate
            FRAMES.append(frameL+frameR)
    return FRAMES
