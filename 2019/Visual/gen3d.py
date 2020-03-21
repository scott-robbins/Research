from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import random
import time
import os

ani_cmd = 'ffmpeg -loglevel fatal -r 3 -i pic%d.png -vcodec libx264 -pix_fmt yuv420p automata3d.mp4'
clean = 'ls *.png | while read n; do rm $n; done'
tic = time.time()
shades = {1: 'red',
          2: 'green',
          3: 'blue',
          4: 'cyan',
          5: 'magenta',
          6: 'orange',
          7: 'yellow',
          8: 'purple'}

width = 50              # TODO: NOTE ** Using width,height,length greater than 50 is probably
length = 50             #  not going to render very well, or may hang system!
height = 50             #
n_steps = 45
k0 = [[1,1,1],[1,0,1],[1,1,1]]

''' DEFINE WORLD DIMENSIONS '''
x, y, z = np.indices((width, length, height))
f = plt.figure()
print '\033[1m#'*int(n_steps/2)+'\033[3m# SIMULATION STARTED #'+'#'*int(n_steps/2)+'\033[0m'

progress = ''
flat = np.zeros((width, length))
for step in range(n_steps):
    circ = imutils.draw_centered_box(flat, step+1, 1, False)
    circ = ndi.convolve(np.random.random_integers(0,1,circ.shape),k0)%3==0
    if step > 0:
        lvl = lvl | (z * circ[x, y] <= step) & (circ[x, y] > 0) & (z > step - 2)
    else:
        lvl = (z*circ[x, y] <= step) & (circ[x, y] > 0) & (z > step-2)
    colors = np.empty(lvl.shape, dtype=object)
    colors[lvl] = shades[np.random.random_integers(1,8,1)[0]]
    ax = f.gca(projection='3d')
    ax.voxels(lvl, facecolors=colors, edgecolors='k')
    plt.savefig('pic%d.png' % step)
    # ax.cla
    # plt.cla
    progress += '*'
    os.system('clear')
    print '#'*int(n_steps/2) + '# SIMULATING ' + '#'*int(n_steps/2)
    print '\033[1m\033[32m%s \033[0m\033[1m[%d percent complete]\033[0m' %\
          (progress, int(step/float(n_steps)*100))

print '#'+'#'*n_steps+' #'
print '\033[31m\033[1mSimulation Finished [%ss Elapsed]\033[0m' % str(time.time()-tic)
print '\033[3mRendering... \033[0m'
os.system(ani_cmd)
os.system(clean)
os.system('vlc automata3d.mp4')
if raw_input('Want to save? (y/n): ').upper()=='N':
    os.remove('automata3d.mp4')
