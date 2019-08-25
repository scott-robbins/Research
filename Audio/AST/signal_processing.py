import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import audiolib
import time
import sys
import os


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
            Tracks.append(audiolib.load_track(m, True))
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
    # audiolib.show_frequencies(titles[choice][0],titles[choice][1],titles[choice][2])
    L = data[:, 0]
    R = data[:, 1]


# TODO: DEBUG/DEVELOPING
song = 'test.mp3'
sample = song.split('.')[0]+'.wav'
if len(sys.argv) >= 2:
    song = sys.argv[1]
cmd = 'ffmpeg -loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s' %\
      (song, sample)
os.system(cmd)
title = audiolib.load_track(sample, False)
name = title['file']
data = title['audio']
samp = title['sample_rate']
title = [name, samp, np.array(data)]


song = []
n_slices = int(data.shape[0]/float(samp))

# TODO: Would be better to make short frames
#  of say window:25ms, step 10ms, N: 512
for slice in range(n_slices):
    if slice > 0:
        chunk = np.array(data[(slice - 1) * samp:samp*slice, 0])
        FFTS = np.fft.rfft(chunk)
        note = np.array(abs(FFTS))[0:20000]
        top = np.array(note).max()
        notes = []
        ind = 0
        for point in note:
            if point >= 0.8 * top:
                notes.append(ind)
            ind += 1
        notes = set(notes)
        print notes

f, ax = plt.subplots(2, 1, sharex=True)
ax[0].grid()
ax[1].grid()
ax[0].plot(chunk)
ax[1].plot(note)
plt.show()

os.remove(sample)