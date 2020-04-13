import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from tqdm import tqdm
import fake_data_gen
import numpy as np
import time
import sys
import os


def generate_training_data(raw_data_path):
    # Generate Fake Training Data
    if os.path.isdir(raw_data_path):
        if 'Circle' not in os.listdir(raw_data_path):
            fake_data_gen.generate_circle_data(raw_data_path, W, H, N)
        else:
            print '[*] Circle Training Data Already Found '
        if 'Square' not in os.listdir(raw_data_path):
            fake_data_gen.generate_square_data(raw_data_path, W, H, N)
        else:
            print '[*] Square Training Data Already Found '
    else:
        fake_data_gen.generate_circle_data(raw_data_path, W, H, N)
        fake_data_gen.generate_square_data(raw_data_path, W, H, N)


def load_training_data(raw_data_path):
    training_data = {}
    labels = os.listdir(raw_data_path)
    dx = [];    dy = []
    for classname in labels:
        training_data[classname] = []
        classpath = '%s/%s' % (raw_data_path, classname)
        print '[*] Loading Training Data: %s/%s' % (raw_data_path, classname)
        for img_file in tqdm(os.listdir(classpath)):
            im = np.array(plt.imread('%s/%s'%(classpath,img_file)))
            training_data[classname].append(im)
            dx.append(im.shape[0])
            dy.append(im.shape[1])
    # Make sure they're all the same shape
    if len(np.unique(dx).flatten()) > 1:
        print '[!!] Multiple X-Dimensions in Training Data'
    if len(np.unique(dy).flatten()) > 1:
        print '[!!] Multiple Y-Dimensions in Training Data'
    return training_data


def edge_detector_bw(img_arr, show):
    w = img_arr.shape[0]
    h = img_arr.shape[1]
    Ey = horizontal_edge_detect(img_arr, 0, h)
    Ex = vertical_edge_detect(img_arr, 0, w)
    actX = np.array(Ex).mean()
    actY = np.array(Ey).mean()
    points = []
    edges = np.zeros((w,h,3))
    for i in range(len(Ey)):
        for j in range(len(Ex)):
            Fy = Ey[i]
            Fx = Ex[j]
            # Now Based on Convolution Of Ex*Ey determine an points of edges
            edges[i, j,1] = Fx*Fy
            if Fx >= actX and Fy >= actY:
                points.append([j, i])
    edges[:, :, 0] = img_arr
    edges[:, :, 2] = img_arr
    # Plot Edge Detection Signals
    if show:
        f, ax = plt.subplots(1, 3, sharex=True)
        ax[0].imshow(edges)
        ax[1].plot(np.array(Ey))
        ax[1].set_xlabel('Row Y')
        ax[2].plot(np.array(Ex))
        ax[2].set_xlabel('Row X')
        plt.show()
        plt.close()

    return points


def horizontal_edge_detect(im_arr, yi, yj):
    Yx = []
    img = np.array(im_arr)
    window_size = (yj - yi)
    for x in range(img.shape[0]):
        Yx.append(np.sum(img[x, yi:yj])/window_size)
    return Yx


def vertical_edge_detect(im_arr, xi, xj):
    Xy = []
    img = np.array(im_arr)
    window_size = (xj - xi)
    for y in range(img.shape[1]):
        Xy.append(np.sum(img[xi:xj, y])/window_size)
    return Xy


W, H, = 550, 550
N = 200
data_path = 'ToyData'
generate_training_data(data_path)
raw_training_data = load_training_data(data_path)


test_image_1 = raw_training_data['Square'][10]
square_points = edge_detector_bw(test_image_1, False)
print '[*] %d Points Detected INSIDE Square' % len(square_points)

test_image_2 = raw_training_data['Circle'][1]
circle_points = edge_detector_bw(test_image_2, True)
print '[*] %d Points Detected INSIDE Circle' % len(circle_points)



