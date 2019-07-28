import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import os

tic = time.time()


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def create_stego(file_name, image_in, preview):
    print 'Extracting Data From %s' % file_name
    data_in = []
    for line in swap(file_name, False):
        for element in line:
            data_in.append(ord(element) / 256.)
        data_in.append(ord('\n') / 256.)

    print '%d Codepoints in Input Data [%ss Elapsed]' % (len(data_in), str(time.time() - tic))
    N =len(data_in)
    # Make BLOCKS?
    # for pad in range(int(N * N - len(data_in))):
    #     data_in.append(0)
    # test_matrix = np.array(data_in).reshape((N, N))
    # print 'Added %d Padding to make %dx%d image from codepoints' % ((N * N) - n0, N, N)

    test_image = plt.imread(image_in)

    rch = test_image[:, :, 0].flatten()
    for ii in range(len(test_image[:, :, 0].flatten())):
        try:
            rch[ii] = data_in.pop()
        except:
            pass
    # RECREATE NEW IMAGE WITH STEGO ADDED
    image = np.zeros(test_image.shape)
    image[:, :, 0] = rch.reshape(test_image[:, :, 0].shape)
    image[:, :, 1] = test_image[:, :, 1]
    image[:, :, 2] = test_image[:, :, 2]
    if preview:
        plt.imshow(image)
        plt.show()

        f, ax = plt.subplots(1, 3)
        ax[0].imshow(test_image)
        ax[0].set_title('Original Image')
        ax[1].imshow(image)
        ax[1].set_title('Stego Image')
        ax[2].imshow(image - test_image)
        ax[2].set_title('Difference')
        plt.show()
    return image, N


def recover_data(image, N, file_out):
    data_out = ''
    matrix = image[:, :, 0].flatten()
    for j in range(N, 0, -1):
        if j > 0:
            data_out += chr(int(matrix[j] * 256.))
    open(file_out, 'w').write(data_out)
    return data_out


if len(sys.argv) > 1:
    file_name = sys.argv[1]
    images = {}
    # TODO: Explicity parse different file types
    image, N = create_stego(file_name,'frame1.png', False)

    ''' REDCOVER INFO '''
    data_out = recover_data(image, N, 'example.c')
