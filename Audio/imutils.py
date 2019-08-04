import numpy as np
import sys
import os


def spawn_random_point(w, h):
    x = np.random.random_integers(0, w, 1)[0]
    y = np.random.random_integers(0, h, 1)[0]
    return [x, y]
