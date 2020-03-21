from  matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()
colors = {1: [1,0,0], 2: [0,1,0], 3: [0,0,1],
          4: [1,0,1], 5: [1,1,0], 6: [0,1,1],
          7: [1,1,1], 8: [0,0,0]}

colormap = {1: 'red', 2: 'green', 3: 'blue',
            4: 'magenta', 5: 'yellow', 6: 'cyan',
            7: 'white', 8: 'black'}

k0 = [[1,1,1],[1,0,1],[1,1,1]]


class Pxl:
    x = 0
    y = 0
    position = 0
    history = []
    value = [0, 0, 0]
    dR = 0

    def __init__(self, pos, val):
        self.x = pos[0]
        self.y = pos[1]
        self.position = [self.x, self.y]
        self.value = val

    def update(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.history.append(self.position)
        self.position = [self.x, self.y]


def simulator(depth, initial_state, start, show):
    if show:
        f = plt.figure()
        film = []
        film.append([plt.imshow(initial_state)])
    history = [start]
    ant = Pxl(start,[1, 0, 0])
    children = []
    while len(history) < depth:
        flip = np.random.random_integers(1, 9, 1)[0]
        moves = {1: [ant.x - 1, ant.y - 1], 2: [ant.x, ant.y - 1], 3: [ant.x + 1, ant.y - 1],
                 4: [ant.x - 1, ant.y], 5: [ant.x, ant.y], 6: [ant.x + 1, ant.y],
                 7: [ant.x, ant.y + 1], 8: [ant.x, ant.y + 1], 9: [ant.x + 1, ant.y + 1]}
        try:
            next_position = moves[flip]
            ant.update(next_position)

            '''
            EVALUATE NEXT POSITION 
            If it isnt maximizing goal consider alternative moves 
            '''
            terrain = ndi.convolve(initial_state[:, :, 2], k0)
            tavg = terrain.mean()
            r = imutils.get_dist(ant.position, start)
            for ii in range(1, len(moves.keys()) + 1, 1):
                [x, y] = moves[ii]
                if imutils.get_dist([x, y], start) > r and terrain[x, y] <= tavg:
                    ant.update([x, y])
                    initial_state[x - 1:x + 1, y - 1:y + 1, 1] += 1
                    initial_state[x - 1:x + 1, y - 1:y + 1, 2] = 0
                    # print imutils.get_dist([x,y],start)
                    initial_state[x, y, 2] += terrain[x, y]
                    continue
            ant.update(next_position)
            initial_state[ant.x, ant.y, :] = ant.value
            film.append([plt.imshow(initial_state)])
            history.append(next_position)
        except IndexError:
            # print '!! %d" % len(history)
            pass

    if show:
        a = animation.ArtistAnimation(f, film, interval=30, blit=True, repeat_delay=900)
        print '[FINISHED %ss Elapsed]' % str(time.time() - tic)
        plt.show()

    return history

# Defaults
w = 250
h = 250
depth = 500
# Add Noise

# or let user define the dimensions
if '-dims' in sys.argv and len(sys.argv) >=4:
    w = int(sys.argv[2])
    h = int(sys.argv[3])
    print '[*] Using Custom Dimensions [%s,%s]' % (w, h)
noise = np.random.random_integers(0,1,w*h).reshape((w, h))
state = np.zeros((w, h, 3))
state[:,:,2] = noise
start = [int(w/2), int(h/2)]

walk = simulator(depth, state, start, True)
print '[FINISHED %ss Elapsed]' % str(time.time()-tic)
