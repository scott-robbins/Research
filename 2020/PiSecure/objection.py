import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import random
import imutils
import time
import os


def pull_random_images(im_path, N):
    images = {}
    im_names = list(os.listdir(im_path))
    random.shuffle(im_names)
    for random_image in range(N):
        im_name = im_names.pop()
        images[im_name] = np.array(plt.imread(im_path+'/'+im_name))
    print '[*] %d Images Loaded from %s' % (N, im_path)
    return images


def subdivide(image, N):
    options = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    if N not in options:
        print '[!!] %d is an not options for subdivisions' % N
    dxs = np.linspace(0, np.array(image).shape[0], N).astype(np.int)
    dys = np.linspace(0, np.array(image).shape[1], N).astype(np.int)
    ii = 0
    cells = {}
    for x2 in dxs:
        i1 = 0
        for y2 in dys:
            if i1 > 0:
                x1 = dxs[i1-1]
                y1 = dys[i1-1]
                square = image[y1:y2, x1:x2]
                cells[ii] = square
            i1 += 1
            ii += 1
    return cells


# TODO: Make this something you get from user input, while testing it's hardcoded
test_path = '/home/tylersdurden/Desktop/Crawler/timelapse/POV1/HasObjects'
train_path = '/home/tylersdurden/Desktop/Crawler/timelapse/POV1/N0'
test_image_names = os.listdir(test_path)
train_image_names = os.listdir(train_path)

# Load Images
averaging_depth = 25
base_images = pull_random_images(train_path, averaging_depth)
test_images = pull_random_images(test_path, 1)
test_image = test_images[test_images.keys().pop()]

# Train Images are used to created an averaged/composite image
# Detection is done by comparing an input with this averaged image
b0 = base_images[base_images.keys().pop()]
sum = np.zeros(b0.shape)
for name in base_images.keys():
    sum[:,:,1] += base_images[name][:,:,1]
    sum[:,:,2] += base_images[name][:,:,2]

# Testing this averaging technique
composite = np.zeros(b0.shape)
composite[:,:,1] = np.abs(1 - (sum[:,:,1])/(averaging_depth*64))
composite[:,:,2] = np.abs(1 - (sum[:,:,2])/(averaging_depth*64))
# composite[:,:,2] = (sum[:,:,2])/(averaging_depth*64)

# detector = (composite[:,:,2] * test_image[:,:,2])  # Points greater than 1 were from test_image
detector = np.zeros((test_image.shape))
detector = test_image[:,:,1] - 128*composite[:,:,1]
detector = test_image[:,:,2] - 255*composite[:,:,2]

# Show the result
f, ax = plt.subplots(1, 2, sharex=True,sharey=True)
# ax[0].imshow(test_image)
# ax[1].imshow(test_image - composite)
# plt.show()

slices = subdivide(test_image, 8)
ax[0].imshow(slices[1])
ax[1].imshow(slices[2])
plt.show()
