import numpy as np
import imutils

known_colors = {'r': [1, 0, 0],
                'g': [0, 1, 0],
                'b': [0, 0, 1],
                'c': [0, 1, 1],
                'm': [1, 0, 1],
                'y': [1, 1, 0]}


def add_even_particle_mix(state, n_total, colors):
    extra = 0
    pix_per_col = int(np.floor(n_total/float(len(colors))))
    if pix_per_col != n_total/len(colors):
        extra = len(colors) - pix_per_col
        print '[*] Overflow: %d' % extra
        print 'Total: %d, Pix-Per-Color: %d N-Colors: %d' %\
              (n_total, pix_per_col, len(colors))
    px_added = {'r': [],'g': [],'b': [],'c': [],'m': [],'y': []}
    while len(colors)>=1:
        if extra and len(colors)==1:
            pix_per_col += extra
        color = colors.pop()
        if color not in known_colors.keys() and px_added.keys():
            print '[!!] Unknown Color: %s' % color
        c = known_colors[color]
        while len(px_added[color]) < pix_per_col:
            try:
                [x, y] = imutils.spawn_random_point(state)
                state[x, y, :] = c
                px_added[color].append([x, y])
            except IndexError:
                pass
    return state, px_added


def add_custom_particle_mix(state, mixture):
    px_added = {'r': [], 'g': [], 'b': [], 'c': [], 'm': [], 'y': []}
    for c in mixture.keys():
        for pt in range(mixture[c]):
            color = known_colors[c]
            added = False
            while not added:
                try:
                    [x,y] = imutils.spawn_random_point(state)
                    state[x,y,:] = color
                    added = True
                    px_added[c].append([x,y])
                except IndexError:
                    pass
    return state, px_added


class Particle:
    x = 0
    y = 0
    color = [0,0,0]
    energy = 0
    steps = []
    style = ''
    known_colors = {'r': [1, 0, 0], 'g': [0, 1, 0], 'b': [0, 0, 1],
                    'c': [0, 1, 1], 'm': [1, 0, 1], 'y': [1, 1, 0]}

    def __init__(self, location, label, e):
        self.x = location[0]
        self.y = location[1]
        if label in self.known_colors.keys():
            self.color = self.known_colors[label]
            self.style = label
        else:
            print '[!!] Unknown Color %s' % label
            return
        self.energy = e

