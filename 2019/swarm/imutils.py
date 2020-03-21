import numpy as np
import random
import time
import os


def swap(file_name, destroy):
    """
    SWAP will open a file, read all of the lines,
    delete the file if destroy flag is set, and return
    the line-by-line data as a list of strings (trailing \n removed)
    :param file_name:
    :param destroy:
    :return:
    """
    data = []
    for line in open(file_name, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(file_name)
    return data


def add_random_points(state, n_points, size):
    """
    ADD_RANDOM_POINTS will take a given state (2D or 3D matrix) and
    spawn random number of points (given as n_points).
    :param state:
    :param n_points:
    :return:
    """
    points = []
    while len(points) < n_points:
        try:
            [x, y] = spawn_random_point(state.shape)
            state[x-size:x+size, y-size:y+size] = 1
            points.append([x, y])
        except IndexError:
            pass
    return state, points


def function_timer(func, args):
    """
    Time how long it takes for any arbitrary function to return a result
    :param func:
    :param args:
    :return:
    """
    start = time.time()
    if args:
        result = func(args)
    else:
        result = func()
    delta = time.time() - start
    # Todo: How to make function call w/ generic **kwargs
    return result, delta


def spawn_random_point(dims):
    """
    SPAWN_RANDOM_POINT will an [x, y]
    :param dims:
    :return:
    """
    x = random.randint(0, dims[0])
    y = random.randint(0, dims[1])
    return x, y


def flat_map(dims):
    """
    FLAT_MAP is useful for pre-allocating a dictionary of index-to-subscript
    lookups on 2D matrix positions. This is particularly useful if any loop
    contains translating coordinates from a flattened 2D array.
    :param dims:
    :return:
    """
    xmax = dims[0]
    ymax = dims[1]
    ind2sub = {}
    ii = 0
    for x in range(xmax+1):
        for y in range(ymax+1):
          ind2sub[ii] = [x, y]
          ii += 1
    return ind2sub


def get_displacement(x1, x2, y1, y2):
    """
    GET_DISPLACEMENT
    Returns the displacement between two points (2D).
    :param x1:
    :param x2:
    :param y1:
    :param y2:
    :return:
    """
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

