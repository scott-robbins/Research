from __future__ import absolute_import, division, print_function, unicode_literals
from tensorflow import keras
import tensorflow as tf
import numpy as n
import Cards
import utils
import time

print(tf.__version__)
tensorboard_cmd = 'tensorboard --logdir=logs/visualize_graph --host localsts'

imdb = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

print('Example Test Data: %s' % str(test_data[0]))
print('Example Test Label: %s' % str(test_labels[0]))

