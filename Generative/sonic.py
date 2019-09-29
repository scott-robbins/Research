from scipy.io import wavfile
import tensorflow as tf
import pandas as pd
import numpy as np
import time
import sys
import os


def load_audio(file_name):
    song = {}
    sample_rate, raw_data = wavfile.read(file_name)
    song['sample_rate'] = sample_rate
    song['data'] = raw_data
    return song


def generate_audio(notes, durations, name):
    audio_data = []
    ii = 0
    for note in notes:
        dt = durations[ii]*44100
        duty = 1/note * 44100
        print duty
        for jj in range(dt):
            audio_data.append(np.sin(duty*jj))
        ii += 1
    print np.array(audio_data).shape
    wavfile.write(name,44100,np.array(audio_data))


# I know I know the theory here is being ignored with sharps but I'm just going for it
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
# For now just spanning 3 octaves [3-5]
notes = {'A': [55, 110, 220, 440, 880],
         'A#': [58.27, 116.54,223.08, 466.16, 932.33],
         'B': [61.74, 123.47, 246.94, 493.88, 987.77],
         'C': [65.41, 130.81, 261.63, 523.25, 1046.55],
         'C#': [69.30, 138.59, 277.18, 554.37, 1108.73],
         'D': [73.42, 146.83, 293.66, 587.33, 1174.51],
         'D#': [77.48, 155.56, 311.13, 622.25, 1244.51],
         'E': [82.41, 164.81, 329.63, 659.25, 1318.51],
         'F': [87.31, 174.61, 349.61, 698.46, 1396.91],
         'F#': [92.5, 185, 369.99, 739.99,  1479.98],
         'G': [98, 196, 392, 783.99, 1567.98],
         'G#': [103.83, 207.65, 415.3, 830.61, 1661.22]}

if '-gen' in sys.argv:
    tone_sequence = ['A', 'B', 'C', 'D']
    tonics = []  # Will do this for octave 3
    [tonics.append(notes[i][1]) for i in tone_sequence]

    print 'Using Tonic Sequence [Hz]: %s' % str(tonics)
    generate_audio(tonics, [1, 1, 1, 1], 'test.wav')

    print 'Generation Finished. Playing Test.wav...'
    # Listen to what is generated
    os.system('paplay test.wav')
    os.system('rm test.wav')
