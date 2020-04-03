
import local_datasets
import numpy as np
import time

tic = time.time()

data_path_1 = '/home/tylersdurden/Desktop/Crawler/timelapse/AI/Negative'
data_path_2 = '/home/tylersdurden/Desktop/Crawler/timelapse/AI/Positive'

packed_imgs_1, labels1 = local_datasets.load_images(data_path_1,{'x0':1200,
                                                                 'x1':1800,
                                                                 'y0':600,
                                                                 'y1':1200,
                                                                 'is':True})

packed_imgs_2, labels2 = local_datasets.load_images(data_path_2,{'x0':1200,
                                                                 'x1':1800,
                                                                 'y0':600,
                                                                 'y1':1200,
                                                                 'is':True})
x_train = local_datasets.image_data_to_tensor(packed_imgs_1)
x_train = local_datasets.image_data_to_tensor(packed_imgs_2)

