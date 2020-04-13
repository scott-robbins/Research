import matplotlib.pyplot as plt
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.models import load_model
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Dense
from keras import models
from tqdm import tqdm
import numpy as np
import pickle
import random
import cv2
import os

DATADIR = "/home/tylersdurden/Desktop/Crawler/timelapse/AI"
CATEGORIES = ["Negative", "Positive"]
IMG_SIZE = 150


def create_training_data():
    training_data = []
    ii = 0
    for category in CATEGORIES:  # do dogs and cats
        path = os.path.join(DATADIR,category)  # create path to dogs and cats
        # class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=dog 1=cat
        class_num = ii
        for img in tqdm(os.listdir(path)):  # iterate over each image per dogs and cats
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass
        ii += 1
    random.shuffle(training_data)
    X = []
    y = []

    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    pickle_out = open("X.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()

    pickle_in = open("X.pickle", "rb")
    X = pickle.load(pickle_in)

    pickle_in = open("y.pickle", "rb")
    y = pickle.load(pickle_in)

    return training_data, X, y


def pre_process_single_img(img):
    img_array = np.array(plt.imread(img).astype(np.float))
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    vec = []
    vec.append(new_array)
    X = []
    for features in vec:
        X.append(features)
    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    X = X / 255.0
    return X


def build_network(Xdat):
    model = models.Sequential()

    model.add(Conv2D(256, (3, 3), input_shape=Xdat.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(256, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(64))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


if __name__ == '__main__':
    if not os.path.isfile('X.pickle') and not os.path.isfile('y.pickle'):
        os.system('python fake_data_gen.py')
        # This will create training data from given datadir and categories
        # Training data is saved to disk for easy reloading
        data, X, y = create_training_data()
    else:
        # Now use our custom data set!
        pickle_in = open("X.pickle", "rb")
        X = pickle.load(pickle_in)
        pickle_in = open("y.pickle", "rb")
        y = pickle.load(pickle_in)
    X = X / 255.0

    '''             BUILD NETWORK              '''
    if not os.path.isfile('model.h5'):
        m = build_network(X)
        '''             TRAIN NETWORK       '''
        # Only using 3 Training Epochs for now
        m.fit(X, y, batch_size=32, epochs=4, validation_split=0.4)
        # Save the Model
        m.save('model.h5')
    else:
        print '\033[1m\033[31m[*] Loading Pre-Trained Model\033[0m'
        m = load_model("model.h5")

    os.remove('X.pickle')
    os.remove('y.pickle')
    test_A = pre_process_single_img('ToyData/Square/square177.png')
    test_B = pre_process_single_img('ToyData/Circle/circle99.png')
    os.system('clear')
    print m.summary()
    print 'Square Prediction: %s Correct: %s' %\
          (str(m.predict_classes(test_A)[0]), m.output_names)

