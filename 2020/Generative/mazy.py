import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import scipy.misc
import imutils
import time
import sys
import os


W = 250
H = 250
n_gen = 5
state = np.zeros((W, H))
ind2sub = imutils.ind2sub(state.shape)
minima = 0
maxima = 1

k = [[1,1,1],[1,0,1],[1,1,1]]

# Add Noise to seed the algorithm
state += np.random.random_integers(minima,maxima,W*H).reshape((W, H))

for generation in range(n_gen):
    # Survive if 1 < x < 4( or 5)
    # Born if x == 3
    world = ndi.convolve(state,k,origin=0)
    for ii in range(len(state.flatten())):
        [x,y] = ind2sub[ii]
        if 1 < world[x, y] < 4:
            state[x, y] = 1
        elif world[x,y] == 3:
            state[x,y] = 1
maze = state
scipy.misc.imsave('maze.png', maze)
