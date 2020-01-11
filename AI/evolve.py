from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import sys
import os


k0 = [[1,1,1,1,1,1],
      [1,0,0,0,0,1],
      [1,0,0,0,0,1],
      [1,0,0,0,0,1],
      [1,0,1,1,0,1],
      [1,1,1,1,1,1]]


class Colors:
    names = ['red', 'green', 'blue', 'cyan',
             'magenta', 'white', 'black']
    hues = {'red':   [1,0,0], 'green' :  [0,1,0], 'blue' : [0,0,1],
            'cyan':  [0,1,1], 'magenta': [1,0,1], 'white': [1,1,1],
            'black': [0,0,0]}
    shade = []

    def __init__(self, n):
        self.shade = self.hues[n]


class Cell:
    x = 0
    y = 0
    position = []
    state = [[]]
    value = []

    def __init__(self, location, color):
        self.initialize(location, color)

    def initialize(self, p, c):
        self.set_pos(p)
        try:
            self.value = Colors.hues[c]
        except KeyError:
            print 'Invalid Color!'

    def set_pos(self, point):
        self.state[self.x, self.y, :] = 0
        self.x = point[0]
        self.y = point[1]
        self.position = [self.x, self.y]
        self.state[self.x, self.y, :] = [1, 0, 0]

    def move(self, n_steps):
        moves = []
        for step in range(n_steps):
            directions = {1: [self.x - 1, self.y - 1], 2: [self.x, self.y - 1], 3: [self.x + 1, self.y - 1],
                          4: [self.x - 1, self.y], 5: [self.x, self.y], 6: [self.x + 1, self.y],
                          7: [self.x - 1, self.y + 1], 8: [self.x, self.y + 1], 9: [self.x + 1, self.y + 1]}
            for n in directions.keys():
                world = ndi.convolve(self.state, k0, origin=0)
                move = directions[n]
                opt = self.state[move[0], move[1]]
                if (opt[0] and opt[1]) == 0 and opt[2] == 1 and world[self.x, self.y]==0:
                    self.state[self.x, self.y, :] = 0
                    moves.append(move)
                    self.set_pos(move)
                    break
        return moves


if __name__ == '__main__':
    ''' Create World '''
    W = 250
    H = 250
    world = np.zeros((W, H, 3))
    world[:,:,2] += np.random.random_integers(0,255,W*H).reshape((W, H)) > 128

    ''' Define Simulation Parameters'''
    depth = 1000
    n_cells = 100

    organisms = []
    for i in range(n_cells):
        [x,y] = imutils.spawn_random_point(world[:,:,2])
        fly = Cell([x,y], 'red')
        organisms.append(fly)
    plt.imshow(fly.state)
    plt.show()
