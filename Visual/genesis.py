from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import os

k0 = [[1,1,1],[1,0,1],[1,1,1]]

ani_cmd = 'ffmpeg -r 1 -f image2 -i pic%d.png -vcodec libx264 -pix_fmt yuv420p sim3d.mp4'

# prepare some coordinates
x, y, z = np.indices((25, 25, 8))

# Start with 2D Bit-Plane
width  = 25
height = 25
plane = np.random.random_integers(0, 255, width*height).reshape((width, height))
s0 = plane > 128
s1 = plane < 128

shades = {1: 'red',
          2: 'green',
          3: 'blue',
          4: 'cyan',
          5: 'magenta',
          6: 'orange',
          7: 'yellow',
          8: 'purple'}

T = 4
B = 1
Depth = 10

''' 3D Simulation! '''
obj = (x > B) & (y > B) & (z > B) & (x < T) & (y < T) & (z > T)
voxels = obj
fig = plt.figure()
ax = fig.gca(projection='3d')

for step in range(Depth):
    # Center Object
    c = np.random.random_integers(1,8,1)[0]
    bits = np.random.random_integers(0, 1, width*height).reshape((width, height))
    obj2 = (T > z) & bits[x, y] & (z > T-2)
    # combine the objects into a single boolean array
    voxels = obj | obj2
    # set the colors of each object
    colors = np.empty(voxels.shape, dtype=object)
    colors[obj] = 'red'
    colors[obj2] = shades[c]
    ax.voxels(voxels, facecolors=colors, edgecolor='k')
    plt.savefig('pic%d.png'%step)
    plt.cla
    T += 1
    B += 1

os.system(ani_cmd)
os.system('clear; ls *.png | while read n; do rm $n; done')
os.system('vlc sim3d.mp4')