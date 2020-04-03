import numpy as np
import time
import os


def ind2sub(dims):
    i2s = {}
    ii = 0
    for x in range(dims[0]):
        for y in range(dims[1]):
            i2s[ii] = [x, y]
            ii += 1
    return i2s

