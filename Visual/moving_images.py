import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()

snip_cmd = 'ffmpeg -ss 00:08:00 -i Video.mp4 -ss 00:01:00 -t 00:01:00 -c copy VideoClip.mp4'

def get_images(verbose):
    frames = []
    os.system('ls *img*.jpg >> pics.txt')
    for fname in open('pics.txt', 'r').readlines():
        frame = np.array(plt.imread(fname.replace('\n', '').replace(' ', '')))
        frames.append(frame)
    if verbose:
        print '%d Frames Extracted ' % len(frames)
        print 'Image(s) Dimensions: %s ' % str(frame.shape)
        print '[%ss Elapsed]' % str(time.time()-tic)
    return frames


def experiment(images_in, show):
    print '[*] Experiment Started'
    n_frames = 0
    frames = []
    if show:
        f = plt.figure()
    for im in images_in:
        mean = np.zeros(im.shape)
        mean[:, :, 0] = im[:, :, 0] - im[:, :, 0].mean()
        mean[:, :, 1] = im[:, :, 1] - im[:, :, 1].mean()
        mean[:, :, 2] = im[:, :, 2] - im[:, :, 2].mean()
        edges = ndi.gaussian_laplace(mean, sigma=1)

        if 'slower' in show.keys():
            for ix in range(show['slower']):
                frames.append([plt.imshow(im*edges)])
                n_frames += 1
        else:
            frames.append([plt.imshow(im * edges)])
            n_frames += 1
    a = animation.ArtistAnimation(f,frames,interval=show['frame_rate']/2, blit=True, repeat_delay=900)
    print 'Finished Simulation. [%ss Elapsed]' % str(time.time()-tic)
    print '[Rendering %d Frames]' % n_frames
    if show['save']:
        writer = animation.FFMpegWriter(fps=show['frame_rate'],metadata=dict(),bitrate=1800)
        a.save(show['name'], writer)
    if show['show']:
        plt.show()


base_cmd = 'ffmpeg -loglevel quiet -i '
extract_frame_cmd = ' -vf fps=1 img%03d.jpg -hide_banner'
file_in = 'herm_tre.mkv'

''' Choose How to Process the Images '''
if len(sys.argv) >= 3:
    file_in = sys.argv[2]

''' Convert Video to Images '''
test_cmd = base_cmd + file_in + extract_frame_cmd
os.system(test_cmd)

''' Load Images into Program'''
images = get_images(verbose=True)


if '-t' in sys.argv:   # Test Mode
    experiment(images, show={'frame_rate': 20,
                             'show': True,
                             'slower': 1,
                             'faster': 0,
                             'save': False,
                             'name': 'hardflip.mp4'})

''' Clean up! '''
os.system('ls *img*.jpg | while read n; do rm $n; done; rm pics.txt')
