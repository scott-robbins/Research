from scipy.io import wavfile
import scipy.signal as signal
from threading import Thread
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
    cmd = 'ffmpeg --loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s' % (file_path, file_out)
    os.system(cmd)


mp3s = []
tmp_song_store = '../AST/inputs'
for song in os.listdir(tmp_song_store):
    print song
    mp3s.append(song)
MP3toWAV('../AST/inputs/'+mp3s.pop(0))