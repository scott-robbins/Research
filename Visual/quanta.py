from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import tkinter as Tk
import numpy as np
import imutils
import time
import sys

tic = time.time()

k0 = [[1,1,1],
      [1,0,1],
      [1,1,1]]

k1 = [[0,0,0,0],
      [0,1,1,0],
      [0,1,1,0],
      [0,0,0,0]]

k2 = [[1,1,1,1],
      [1,0,0,1],
      [1,0,0,1],
      [1,1,1,1]]


def force_field(pts, nsteps, state):
    f = plt.figure()
    steps = {}
    ii = 0
    for pt in pts:
        steps[ii] = imutils.spawn_random_walk(pt, nsteps)
        ii += 1
    test = []
    for jj in range(nsteps):
        rch = ndi.convolve(state[:, :, 0], k1, origin=0)
        gch = ndi.convolve(state[:, :, 1], k1, origin=0)
        bch = ndi.convolve(state[:, :, 2], k1, origin=0)
        mm = 0
        for px in range(len(pts)):
            [x, y] = steps[px][jj]
            if jj > 0:
                [x0, y0] = steps[px][jj - 1]
                state[x0, y0, :] = 0
                state[x, y, :] += [0, 0, 1]
            mm += 1
        for px in range(len(pts)):
            [x, y] = steps[px][jj]
            if jj > 0:
                [x0, y0] = steps[px][jj - 1]
            if state[x,y,2] == 1 and gch[x,y] >= gch.mean():
                state[x,y,:] = 0
                state[x,y,0] = 1
        # TODO: APPLY CELLULAR AUTOMATA RULES
        state[:, :, 1] += ndi.convolve(bch, k1, origin=0) / np.sum(k2)
        state[:, :, 0] += ndi.convolve(bch, k0, origin=0) / 16.
        test.append([plt.imshow(state)])
    a = animation.ArtistAnimation(f, test, interval=65, blit=True, repeat_delay=900)
    plt.show()
    return state


colors = {'R': [1,0,0],
          'G': [0,1,0],
          'B': [0,0,1],
          'C': [0,1,1],
          'M': [1,0,1],
          'Y': [1,1,0],
          'K': [0,0,0],
          'W': [1,1,1]}

n_particles = 850
n_steps = 100
width = 450
height = 450
state = np.zeros((width, height, 3))
Rad = 85

# draw a centered point cloud (blue particles)
state, points = imutils.draw_blue_point_cloud(width,height,state,n_particles,Rad, False)
print '%d Points in Cloud ' % len(points)
final_state = force_field(points, n_steps, state)
