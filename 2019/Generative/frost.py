from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from tqdm import tqdm
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()

k0 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]

k1 = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]

f1 = [[0, 0,  0, 0.5, 0, 0, 0],
      [0, 0.5, 1, 0, 1, 0.5, 0],
      [0, 1, 0.5, 1, 0.5, 1, 0],
      [0.5, 0, 1, 0, 1, 0, 0.5],
      [0, 1, 0.5, 1, 0.5, 1, 0],
      [0, 0.5, 1, 0, 1, 0.5, 0],
      [0, 0, 0, 0.5, 0, 0, 0]]


def simulation(state, depth, save):
    print '\033[1mRUNNING \033[31mSimulation\033[0m'
    t0 = time.time()
    f = plt.figure()
    film = []
    film.append([plt.imshow(state)])
    bar = tqdm(total=depth)
    for step in tqdm(range(depth)):
        ind2sub = imutils.LIH_flat_map_creator(state[:, :, 0])
        rch = state[:, :, 0]
        gch = state[:, :, 1]
        bch = state[:, :, 2]

        rc0 = ndi.convolve(state[:, :, 0], k0, origin=0)
        gc0 = ndi.convolve(state[:, :, 1], k0, origin=0)
        bc0 = ndi.convolve(state[:, :, 2], k0, origin=0)

        for ii in range(state.shape[0]*state.shape[1]):
            [x, y] = ind2sub[ii]
            if not rch[x,y] and not gch[x,y] and not bch[x,y]:  # Black Pixel
                if bc0[x, y] % 5 == 0:
                    state[x, y, 2] += 1
                if (bc0[x, y] and gc0[x,y]) % 5==0:
                    state[x,y,0] += 1
                # if gc0[x,y] >3:
                #     state[x,y,1] += 1
            if bch[x,y] and not rch[x,y]:
                if bc0[x, y] % 7 == 0:
                    state[x, y, :] -= 1
            if rch[x,y] and not (bch[x,y] or rch[x,y]):
                if rc0[x,y] % 8 ==0:
                    state[x,y,0] -=1
                if bc0[x,y] % 5 == 0:
                    state[x,y,:] = [1, 1, 0]


        if step == int(depth)/2:
            state[:, :, 2] -= imutils.draw_centered_circle(state[:,:,0], 20, .5, False)
            # state[:, :, 1] += state[:, :, 2]
            # state[:, :, 0] += state[:, :, 1]

        film.append([plt.imshow(state)])
        bar.update(1)
    print '\033[1mSimulation FINISHED \033[31m[%ss Elaped]\033[0m' % (time.time()-t0)
    a = animation.ArtistAnimation(f, film, interval=save['frame_rate'],blit=True,repeat_delay=900)
    if save['save']:
        w = FFMpegWriter(fps=save['frame_rate'],bitrate=1800)
        a.save(save['name'], writer=w)
    plt.show()
    return state


''' Define Simulation Parameters'''
width = 250
height = 250
depth = 75
initial_state = np.zeros((width, height, 3))
initial_state[:, :, 2] += np.random.random_integers(0,255,width*height).reshape((width, height)) > 200
initial_state[:,:,1] += initial_state[:,:,2]
''' Run the Simulation '''
simulation(initial_state, depth, {'save': True,
                                  'frame_rate': 200,
                                  'name': 'polarization_2.mp4'})
