import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
import os


def draw_centered_circle(canvas, radius,value, show):
    cx = canvas.shape[0]/2
    cy = canvas.shape[1]/2
    for x in np.arange(cx - radius, cx + radius, 1):
        for y in np.arange(cy - radius, cy + radius, 1):
            r = np.sqrt((x-cx)**2 + ((cy-y)**2))
            if r <= radius:
                try:
                    canvas[x, y] = value
                except IndexError:
                    pass
    if show:
        plt.imshow(canvas, 'gray_r')
        plt.show()
    return canvas


def draw_centered_box(state, sz, value, show):
    cx = state.shape[0]/2
    cy = state.shape[1]/2
    state[cx-sz:cx+sz,cy-sz:cy+sz] = value
    if show:
        plt.imshow(state)
        plt.show()
    return state


w = 550
h = 550

N = 200
os.mkdir('ToyData')
os.mkdir('ToyData/Square')
for i in range(N):
    state = np.zeros((w, h))
    sq = draw_centered_box(state,i+1,1,False)
    name = 'ToyData/Square/square%d.png' % i
    misc.imsave(name, sq)

os.mkdir('ToyData/Circle')
for j in range(N):
    state = np.zeros((w, h))
    circ = draw_centered_circle(state,j+2,1,False)
    name = 'ToyData/Circle/circle%d.png' % j
    misc.imsave(name, circ)
