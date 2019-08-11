import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import utils
import time
import sys
import os

tic = time.time()


def load_training_data():
    Artists = []
    Music = {}
    Total_Songs = 0
    for name in os.listdir('Training/'):
        if len(name.split('.')) == 1:
            Artists.append(name)
            Music[name] = []
            for song in os.listdir('Training/' + name):
                if os.path.isfile('Training/' + name + '/' + song):
                    Music[name].append('Training/' + name + '/'+song)
                elif os.path.isdir('Training/' + name + '/' + song):
                    for track in os.listdir('Training/' + name + '/' + song):
                        Music[name].append('Training/' + name + '/' + song+'/'+track)
            print '  \033[1m[*]\033[33m %s\033[0m (%d songs)' % (name, len(Music[name]))
            Total_Songs += len(Music[name])
    print '\033[1m\033[31m%d\033[0m\033[1m Artists In Training Library\033[0m' % len(Artists)
    print '\033[1m\033[31m%d\033[0m\033[1m Songs In Training Library\033[0m' % Total_Songs
    return Artists, Music, Total_Songs


def load_artist_data(artist, artists):
    artist_tracks = {}
    data_pointers = {}
    print '< Unpacking ARTIST:%s >' % artist
    for track in artists[artist]:
        if os.path.isfile(track):
            if len(track.split(' '))<=1:
                n = track.split('/').pop()
                if n.split('.')[1] == 'mp3':
                    m = n.split('.')[0].replace("'",'')+'.wav'
                    print 'Converting %s to WAV File ...' % track
                    cmd = 'ffmpeg -loglevel quiet -i %s -ar 44100 -ac 2 -b:a 192k %s' % (track, m)
                    os.system(cmd)

            elif 'mp3' in track.split('.'):
                n = track.split('/').pop()
                m = n.split('.')[0].replace(' ','').replace("'",'')+'.wav'
                print 'Converting %s to WAV File ...' % track
                os.system('ffmpeg -loglevel quiet -i "%s" -ar 44100 -ac 2 -b:a 192k %s' % (track, m))
            sample_rate, audio_raw = wavfile.read(m)
            artist_tracks[track] = [sample_rate, audio_raw]
    return artist_tracks


if os.path.isdir('Training'):
    os.system('find -name *.wav | cut -b 3- | while read n; do echo $n >> wavs.txt; done')
    os.system('find -name *.mp3 | cut -b 3- | while read n; do echo $n >> mp3s.txt; done')

    mp3_files_in = utils.swap('mp3s.txt', True)
    wav_files_in = utils.swap('wavs.txt', True)

    print '[*] %d WAV Files Found \n[*] %d MP3 Files Found ' % (len(wav_files_in),len(mp3_files_in))
    print '\033[1m\033[3m\033[32mArtists Found:\033[0m'
    artist_names, tracks, n_songs = load_training_data()

else:
    print 'No Training/ Folder Present!'
    exit()

'''
Artists = Categories[0-9] <--> "Name"
Tracks =  Library[Artist][N] <---> [0010110111010]
'''

f = plt.figure()

test_artist = 'Vulfpeck'
# For Debugging I will start with Vulfpeck. Bc, short songs and only a few of them
test_artist_tracks = load_artist_data(test_artist, tracks)
print '\033[1m\033[32mPre-Processing Tracks By\033[0m\033[1m %s\033[0m' % test_artist
for track in test_artist_tracks.keys():
    test = np.array(utils.process_song(test_artist_tracks[track], track))
    plt.plot(test)
plt.show()
''' FINISHED '''
os.system('ls *.wav | while read n; do rm "$n"; done') # CLEANUP WAV FILES
print '[\033[1m\033[36m%ss Elapsed\033[0m]' % str(time.time()-tic)