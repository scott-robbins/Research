import matplotlib.pyplot as plt
import scipy.misc as misc
from tqdm import tqdm
import numpy as np
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


def generate_square_data(data_path, W, H, n):
    if not os.path.isdir('%s/Square' % data_path):
        os.mkdir('%s/Square' % data_path)
    print '[*] Generating Square Images'
    for i in tqdm(range(n)):
        state = np.zeros((W, H))
        sq = draw_centered_box(state, i + 1, 1, False)
        name = '%s/Square/square%d.png' % (data_path,i)
        misc.imsave(name, sq)
    print '[*] Finished Generating Square Data'


def generate_circle_data(data_path, W, H, n):
    if not os.path.isdir('%s/Circle' % data_path):
        os.mkdir('%s/Circle' % data_path)
    print '[*] Generating Circle Images'
    for j in tqdm(range(n)):
        state = np.zeros((W, H))
        circ = draw_centered_circle(state, j + 2, 1, False)
        name = '%s/Circle/circle%d.png' % (data_path, j)
        misc.imsave(name, circ)
    print '[*] Finished Generating Circle Data'


if __name__ == '__main__':

    # Dimensions of each test image
    # and number of images per shape
    w = 550
    h = 550
    N = 200

    # Make the ToyData
    os.mkdir('ToyData/')
    generate_circle_data('ToyData', w, h, N)
    generate_square_data('ToyData', w, h, N)

