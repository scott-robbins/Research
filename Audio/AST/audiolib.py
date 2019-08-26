import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy.io import wavfile
from threading import Thread
import numpy as np
import librosa
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


def analyze_music_library():
    tic = time.time()
    os.system('clear')
    Tracks = []
    # Load Samples
    if os.path.isdir('SAMPLES'):
        print '\033[3mLoading Sample Tracks\033[0m'
        for n in os.listdir('SAMPLES'):
            m = n.split('.')[0].replace("'", '') + '.wav'
            track = 'SAMPLES/' + n
            print 'Converting %s to WAV File ...' % ('SAMPLES/' + n)
            cmd = 'ffmpeg -loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s' % (track, m)
            os.system(cmd)
            Tracks.append(load_track(m, True))
            os.system('rm %s' % m)
    else:
        print 'Creating SAMPLES Directory [For Training Data]'
        os.mkdir('SAMPLES')
    print '================================================================='
    # TODO: DEBUGGING - Choose a song at a time to analye
    #  (eventually all sequentially)
    print 'Which song To analyze?:'
    n = 0
    titles = {}
    for title in Tracks:
        n += 1
        name = title['file']
        data = title['audio']
        samp = title['sample_rate']
        titles[n] = [name, samp, np.array(data)]
        print '\t\033[1m[%d]\033[0m %s' % (n, name)
    choice = int(raw_input('Enter a selection: '))
    try:
        print 'Loading %s' % titles[choice][0]
    except KeyError:
        print '\033[1m\033[33mSomething broke...\033[0m'
    L = data[:, 0]
    R = data[:, 1]
    return L, R, titles


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

