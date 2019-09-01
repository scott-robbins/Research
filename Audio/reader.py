from scipy.io import wavfile
from threading import Thread
import numpy as np
import time
import sys
import os

tic = time.time()


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data





def rec(name):
    cmd = 'sox -t alsa default %s &' % name
    os.system(cmd)


def start_recording():
    record = Thread(target=rec, args=('clip.wav',))
    record.start()
    record.join()
    return record


def stop_recording():
    cmd = "ps aux | grep 'sox -t' | cut -b 11-16 | while read n; do echo $n; kill -9 $n; done"
    os.system(cmd)


def snip_audio(start,stop,audio,sampling):
    test_range = audio[start * sample_rate:stop * sample_rate, :]
    wavfile.write('clip.wav', rate=sampling, data=test_range)
    return test_range


def playback(audio_data, sample_rate, volume, delete):
    # TODO: Debugging!
    vol = {}
    i = 0
    for ii in np.linspace(0, 65535, 10):
        vol[i] = ii
        i += 1
    wavfile.write('clip.wav', rate=sample_rate, data=audio_data)
    cmd = 'paplay --volume=%d clip.wav' % (vol[volume])
    print cmd
    os.system(cmd)
    if not delete:
        if raw_input('Delete Clip? [y/n]: ') == 'y':
            os.remove('clip.wav')


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        file_in = sys.argv[1]
        sample_rate, audio = wavfile.read(file_in)
        audio = np.array(audio)
        len_sec = audio.shape[0] / sample_rate
        print audio.shape
        print '~%dm:%ds of audio' % (int(len_sec / 60.0), int(60 * (len_sec / 60. - int(len_sec / 60.))))
        if len(sys.argv) >= 5 and '-snip' in sys.argv:
            start = int(sys.argv[3])
            stop = int(sys.argv[4])
            data = snip_audio(start, stop, audio, sample_rate)
            playback(data, sample_rate, 9, True)

    if 'mon' in sys.argv:
        running = True
        file_in = sys.argv[1]
        n_read = 0
        while running:
            try:
                sample_rate, audio = wavfile.read(file_in)
                audio = np.array(audio)
                print audio.shape
                audio = np.zeros((0, 0))
                time.sleep(0.1)
                n_read += 1
            except KeyboardInterrupt:
                running = False
                break
        print '[*] %d File Reads Executed ' % n_read
    print '[%ss Elapsed] ' % str(time.time() - tic)
