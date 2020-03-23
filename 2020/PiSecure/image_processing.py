import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from scipy import misc
from tqdm import tqdm
import numpy as np
import imutils
import time
import sys
import os


def load_images(dataset, cut):
    isCut = cut['is']
    if isCut:
        x0 = cut['x0'];    y0 = cut['y0']
        x1 = cut['x1'];    y1 = cut['y1']
    image_data = {}
    if not os.path.isdir(dataset):
        print '[!!] Cannot find dataset: %s' % dataset
    tic = time.time()
    classes = os.listdir(dataset)

    # All of the training images can put quite a load on machine, so let user define how deep
    # They want to go here
    CUTOFF = 50
    for class_name in classes:
        class_path = dataset+'/'+class_name
        if os.path.isdir(class_path):
            print '[*] Loading Data From %s' % class_path
            image_data[class_name] = []
            for file in tqdm(os.listdir(class_path)[0:CUTOFF], unit=' file(s)'):
                if not isCut:
                    image_data[class_name].append(np.array(misc.imread(dataset+'/'+class_name+'/'+file)))
                else:
                    im = np.array(misc.imread(dataset+'/'+class_name+'/'+file))[y0:y1, x0:x1, :]
                    image_data[class_name].append(im)

    print '\033[1m================================================================================\033[0m'
    print '\033[1m[*] %d Classes Loaded\033[0m' % len(classes)
    print '\033[1m[*] %d Images in Class < %s >\033[0m' % (len(image_data[classes[0]]), classes[0])
    print '\033[1m[*] %d Images in Class < %s >\033[0m' % (len(image_data[classes[1]]), classes[1])
    print '\033[1m[*] FINISHED [%ss Elapsed] \033[0m' % str(time.time() - tic)
    print '\033[1m================================================================================\033[0m'
    return image_data, classes


def extract_features(eigen, images, i, plot):
    test_im = np.array(images[types[0]][i]).astype(np.float32)
    feature_map = test_im[:,:,0] * eigen[:, :, 0] - test_im[:, :, 0].mean()
    # Show the result
    if plot:
        f, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 8))
        ax[0].imshow(images[types[0]][i])
        ax[1].imshow(feature_map, cmap='hot', interpolation='nearest')
        plt.show()
    return feature_map


def training_pipe(imgs, ts):
    e = np.zeros(imgs[ts[1]].pop().shape).astype(np.float)
    N = len(imgs[ts[1]])
    for im in tqdm(imgs[types[1]], unit=' image(s)'):
        e[:, :, 0] += np.array(ndi.convolve(im[:, :, 0], k)).astype(np.float) / (N)
        e[:, :, 1] += np.array(ndi.convolve(im[:, :, 1], k)).astype(np.float) / (N)
        e[:, :, 2] += np.array(ndi.convolve(im[:, :, 2], k)).astype(np.float) / (N)
    e /= 2. * N
    return e


test_path = '/home/tylersdurden/Desktop/Crawler/timelapse/smart_security'
images, types = load_images(test_path, {'is': True,
                                        'x0': 0,
                                        'y0': 800,
                                        'x1': 2440,
                                        'y1': 1800})
# TODO: Get rid of this later, but now animating all of the images during processing is helpful
# ims = []
# f = plt.figure()
# for train in images[types[1]]:
#     ims.append([plt.imshow(train)])
# for test in images[types[0]]:
#     ims.append([plt.imshow(test)])
# a = animation.ArtistAnimation(f,ims,interval=125,blit=True,repeat_delay=900)
# plt.show()
k = [[1,1,1],[1,0,1],[1,1,1]]

'''     TRAINING_PIPELINE '''
# Layer One - Mean Image Creator
print '[*] Feeding %d Images into Training Data Pipeline' % len(images[types[1]])
avg_img = training_pipe(images, types)

'''     USING TRAINING IMAGE TO EXTRACT FEATURES FROM A TEST IMAGE '''
features = extract_features(avg_img,images,1,True)
