from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.models import Sequential
from keras.datasets import mnist
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(123)  # for reproducibility
np.random.seed(123)  # for reproducibility

# Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)
print 'Test Images:'
print(y_train[4545], y_train[1], y_train[2], y_train[3])

# Reshape Data
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)

# convert data type and normalize values
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

print(y_train[4545])
plt.imshow(X_train[4545][0], cmap=plt.get_cmap('gray'))
plt.title('Test Image #1')
plt.show()

print (y_train.shape)
# Convert 1-dimensional class arrays to 10-dimensional class matrices
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)
print (Y_train.shape)

# Create a Model
model = Sequential()
# Create Input Layer
model.add(Convolution2D(32,(3,3),activation='relu',data_format='channels_first',input_shape=(1,28,28)))
model.add(Convolution2D(32, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
# output 10 classes corresponds to 0 to 9 digits we need to find
model.add(Dense(10, activation='softmax'))

# Build The model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the Model
model.fit(X_train, Y_train,batch_size=32, nb_epoch=10, verbose=1)
score = model.evaluate(X_test, Y_test, verbose=0)
print(score)
if score[1]>0.985:
    # Save the Model
    print '\033[1m[*]\033[31mModel Accuracy is %s. Saving Model.\033[0m' % str(score[1])
    model.save('model.h5')

k = np.array(X_train[4545]) #seven
# Input image array is reshaped into a tensor for model to make a prediction
y = k.reshape(1, 1, 28, 28)
prediction = model.predict(y)
# Show Which Class the Model Predicts (Hopefully 7)
print model.predict_classes(y)

