import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy.io import wavfile
from threading import Thread
import numpy as np
import time
import os


def record_audio(file_name):
    rec_cmd = 'sox -t alsa default %s' % file_name
    os.system(rec_cmd)


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def play(file_name):
    volume = 9
    vol = {}
    i = 0
    for ii in np.linspace(0, 65535, 10):
        vol[i] = ii
        i += 1
    cmd = 'paplay --volume=%d %s' % (vol[volume], file_name)
    print cmd
    os.system(cmd)


def start_recording(file_name):
    record = Thread(target=record_audio, args=(file_name,))
    record.start()
    record.join()
    return record


def stop_recording():
    cmd = "ps aux | grep 'sox -t' | cut -b 11-16 | while read n; do echo $n; kill -9 $n; done"
    os.system(cmd)


def load_track(file_name, verbose):
    track = {}
    sample_rate, audio_data = wavfile.read(file_name)
    track['sample_rate'] = sample_rate
    track['audio'] = np.array(audio_data)
    track['file'] = file_name
    track['length'] = float(track['audio'].shape[0])/sample_rate
    if verbose:
        print '\033[1m%s \033[31mLoaded\033[0m' % file_name
        print '  * %f seconds of Audio Data' % track['length']
        print '  * Sample Rate: %d' % sample_rate

    return track


