import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os


class NPN:
    state = [[]]
    bounds_box_1 = []
    bounds_box_2 = []
    bounds_box_3 = []
    n_charges = 0
    temperature = 0

    def __init__(self, dims, percentage_p):
        self.state = np.zeros((dims[0], dims[1]))


diffusion_reaction = NPN([250, 250], 0.6)

