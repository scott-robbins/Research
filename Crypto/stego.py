import matplotlib.pyplot as plt
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


if 'run' in sys.argv and len(sys.argv) >= 3:
    file_name = sys.argv[2]
    images = {}
    # TODO: Explicity parse different file types
    print 'Extracting Data From %s' % file_name
    data_in = []
    for line in swap(file_name, False):
        for element in line:
            data_in.append(ord(element))
        data_in.append(ord('\n'))
    print '%d Codepoints in Input Data [%ss Elapsed]' % (len(data_in),str(time.time()-tic))

    ''' TESTING STEGO '''
    import test

    ''' GET VIDEO DATA FOR STEGANOGRAPHIC COVER '''
    sample_video_1 = '/home/tylersdurden/Documents/PiCam/code/Examples/mail_truck.mp4'
    sample_video_2 = '/home/tylersdurden/Documents/PiCam/code/Examples/exit.mp4'
    long_video = '/home/tylersdurden/Documents/PySimpleGUI/YoloObjectDetection/videos/car_chase_02.mp4'

    ''' Split Video into images and load those images into program '''
    os.system('ffmpeg -loglevel quiet -i ' + long_video + ' -vf fps=1 frame%d.png -hide_banner')
    os.system('find -name "*frame*.png" | cut -b 3- | while read n; do echo $n >> images.txt; done')
    for frame in swap('images.txt', True):
        num = int(frame.split('frame')[1].split('.')[0])
        images[num] = np.array(plt.imread(frame))
    print '%d Images Indexed [%ss Elapsed]' % (len(images.keys()),str(time.time()-tic))
    N = np.array(images.keys()).max()

    ''' CLEANUP IMAGES ON EXIT '''
    os.system('ls *.png | while read n; do rm $n; done')