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
G = 6.6743e-11


class Particle:
    mass = 0
    size = 0
    rvec = 0
    position = []
    velocity = []

    def __init__(self, m, sz, loc):
        self.mass = m
        self.size = sz
        self.position = loc

    def calculate_gravitational_attraction(self, m2):
        return G*(self.mass*m2.mass)/(self.rvec**2)


def add_particles(world, particle, n):
    points = []
    for pt in range(n):
        try:
            [x, y] = imutils.spawn_random_point(world[:, :, 0])
            world[x, y, 0] = 1
            p = Particle(1, 1, [x, y])
            nx = particle.position[0]
            ny = particle.position[1]
            px = p.position[0]
            py = p.position[1]
            p.rvec = np.sqrt((px - nx) ** 2 + (py - ny) ** 2)
            p.calculate_gravitational_attraction(particle)
            points.append(p)
        except IndexError:
            pass
    return points


def main():
    colors = {'R': [1, 0, 0],
              'G': [0, 1, 0],
              'B': [0, 0, 1],
              'C': [0, 1, 1],
              'M': [1, 0, 1],
              'Y': [1, 1, 0],
              'K': [0, 0, 0],
              'W': [1, 1, 1]}
    width = 250
    height = 250
    n_particles = 100
    state = np.zeros((width, height, 3))

    ''' Adding Electro Circle] '''
    e_sz = 10
    state[:, :, 2] = imutils.draw_centered_circle(state[:, :, 2], e_sz, 1, False)
    nucleus = Particle(10, e_sz, [int(width / 2), int(height / 2)])

    ''' Adding particles '''
    add_particles(state, nucleus, n_particles)



if __name__ == '__main__':
    main()
