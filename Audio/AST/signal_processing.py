import matplotlib.pyplot as plt
import numpy as np
import audiolib
import time
import sys
import os

tic = time.time()

convert_cmd = 'ffmpeg -loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s'
snip_cmd = 'ffmpeg -ss %d -t %d -i %s %s'
N_FILTERS = 4096


def short_time_fast_fourier_transform(content_file, style_file):
    content_spec, fs1 = np.array(audiolib.read_audio_spectum(content_file))
    style_spec, fs2 = np.array(audiolib.read_audio_spectum(style_file))
    N_SAMPLES = content_spec.shape[1]
    N_CHANNELS = content_spec.shape[0]
    a_style = style_spec[:N_CHANNELS, :N_SAMPLES]

    print 'Audio Spectra Mapped [%ss Elapsed' % str(time.time() - tic)
    f, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].set_title('Content')
    ax[0].imshow(content_spec[:400, :])
    ax[1].set_title('Style')
    ax[1].imshow(style_spec[:400, :])
    plt.show()

    a_content_tf = np.ascontiguousarray(content_spec.T[None, None, :, :])
    a_style_tf = np.ascontiguousarray(style_spec.T[None, None, :, :])
    std = np.sqrt(2) * np.sqrt(2.0 / ((N_CHANNELS + N_FILTERS) * 11))
    kernel = np.random.randn(1, 11, N_CHANNELS, N_FILTERS) * std


