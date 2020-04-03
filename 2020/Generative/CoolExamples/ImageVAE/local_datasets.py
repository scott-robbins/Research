import scipy.misc as misc
from tqdm import tqdm
import numpy as np
import  time
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

    return image_data, classes


def image_data_to_tensor(dataset):
    # Get the dimensions of dataset
    classes = list(dataset.keys())
    n_classes = len(classes)
    n_images = 0
    for name in classes:
        n_images += len(dataset[name])
    dims = np.array(dataset[classes[0]][0]).shape

    # Build Tensor
    ii = 0
    T = np.zeros((n_images, dims[0], dims[1], 3))
    print '[*] Building Tensor ...'
    print '[*] Shape: %s' % str(T.shape)
    for label in classes:
        for img in dataset[label]:
            T[ii,:,:,:] = img
            ii += 1
    print '[*] Tensor Created [Shape: %s' % str(T.shape)
    return T

