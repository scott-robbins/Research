import matplotlib.pyplot as plt
from tensorflow import keras 
import tensorflow as tf
import pandas as pd
import numpy as np


RANDOM_SEED = 42
time_steps = 10
np.random.seed(RANDOM_SEED)
tf.random.set_random_seed(RANDOM_SEED)


# Mock Data
time = np.arange(0,100,0.1)
sin = np.sin(time) + np.random.normal(scale=0.5, size=len(time))

plt.plot(time,sin,label='test input (sin + noise)')
plt.legend()
plt.show()

# Data Preprocessing 
df = pd.DataFrame(dict(sine=sin), index=time, columns=['sine'])
df.head()

train_size = int(len(df) * 0.8)
test_size = len(df) - train_size
train, test = df.iloc[0:train_size], df.iloc[train_size:len(df)]
print(len(train), len(test))


def create_dataset(X, y, time_steps=1):
	Xs, ys = [], []
	for i in range(len(X) - time_steps):
		v = X.iloc[i:(i + time_steps)].value
		Xs.append(v)
		ys.append(y.iloc[i+time_steps])
	return np.array(Xs), np.array(ys)


# Reshape to [samples, time_steps, n_features]
X_train, y_train = create_dataset(train, train.size, time_steps)
X_test, y_test = create_dataset(test, test.sine, time_steps)
print(X_train.shape, y_train.shape)

# Modeling
model = keras.Sequential()
model.add(keras.layers.LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(keras.layers.Dense(1))
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.001))

# Training
history = model.fit(X_train,y_train,epochs=30,batch_size=16,validation_split=0.1,verbose=1,shuffle=False)


