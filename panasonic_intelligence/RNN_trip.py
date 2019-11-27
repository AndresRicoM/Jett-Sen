# -*- coding: UTF-8 -*-

#
#         ██╗███████╗████████╗████████╗   ███████╗███████╗███╗   ██╗
#        ██║██╔════╝╚══██╔══╝╚══██╔══╝   ██╔════╝██╔════╝████╗  ██║
#       ██║█████╗     ██║      ██║█████╗███████╗█████╗  ██╔██╗ ██║
#  ██   ██║██╔══╝     ██║      ██║╚════╝╚════██║██╔══╝  ██║╚██╗██║
#  ╚█████╔╝███████╗   ██║      ██║      ███████║███████╗██║ ╚████║
#  ╚════╝ ╚══════╝   ╚═╝      ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═══╝
#
#   Sensorized Panasonic Jetter Hackable Bike - Recurrent Neural Network Program for Classification of Types of Bike States.
#   Andres Rico - MIT Media Lab - aricom@mit.edu - www.andresrico.xyz
#
# Script runs an RNN model on a given data set containing a sequence of data points belonging
# to a specific bike ride. The input data has been pre processed to only contain desired variables (Speed, Torque, Accelerations...
# temperature, humidity and pressure) as well as the clustering values that have been created using K-Means (running unsupervised.py)
#

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, CuDNNLSTM    #add CuDNNLSTM to run in GPU
import numpy as np
import matplotlib.pyplot as plt
#from tensorflow.contrib.rnn import *

CUDA_VISIBLE_DEVICES = 0 
#Access data.
data_path = '/home/andres/Jett-Sen/panasonic_intelligence/clustered_data/'
data_name = 'clustered_Bike_data.txt'

#Format input data.
current_data = np.genfromtxt(data_path + data_name , delimiter = ',',  dtype='str')
X = current_data[:, 1:-2] #Take away timestamp column (column 0)
Y = current_data[:, -1] #Assign class column to Y vector.
X = X.astype(np.float) #Change str to floats.
Y = Y.astype(np.float)

index = int(round(current_data.shape[0] * .7))

x_train = X[0:index,:] #Create X matrix for training.
x_test = X[(index + 1):X.shape[0],:] #Create X matrix for testing.
y_train = Y[0:index] #Create Y label vector for training.
y_test = Y[(index + 1):Y.shape[0]] #Create Y vector for testing.

#Reshapes X matrix to be able to feed in to LSTM.
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
print (x_train.shape)
print (x_test.shape)

#Reshapes target classes for feeding into network.
y_train = np.reshape(y_train, (y_train.shape[0], 1))
y_test = np.reshape(y_test, (y_test.shape[0], 1))
print (y_train.shape)
print (y_test.shape)

#Begin sequential model.
model = Sequential()

#Fisrt layer of model LSTM. input shape expects input of the size of each X instance.

model.add(LSTM(256, input_shape=(1,8), activation='relu', return_sequences=True)) #Uncomment to run on CPU
#model.add(CuDNNLSTM(256, input_shape = (1,8), return_sequences = True)) #Uncomment to run on GPU
model.add(Dropout(0.2))

model.add(LSTM(256, activation = 'relu')) #Uncomment to run on CPU
#model.add(CuDNNLSTM(256)) #Uncomment to run on GPU
model.add(Dropout(0.2))

#Feeds LSTM results into Dense layers for classification.
model.add(Dense(500, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(500, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(500, activation='relu'))
model.add(Dropout(0.2))

#Last layer of model outputs probability of belonging to a class. Classes are assigned by K-means within unsupervised.py
model.add(Dense(5, activation='softmax'))

#Declare optimizing fucntion and parameters.
opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

#Compile model
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy'],
)

#Fit model and store into history variable.
history = model.fit(x_train, y_train, epochs=400, validation_data=(x_test, y_test))

print(history.history.keys()) #terminal outout of accuracy results.

test_loss, test_acc = model.evaluate(x_test, y_test) #Evaluate model with test sets (X and Y).

print('Test accuracy:', test_acc) #Terminal print of final accuracy of model.

#Plot accuracy results of training and test data.
plt.style.use('dark_background')
plt.rcParams.update({'font.size': 25})
plt.figure(1)
plt.plot(history.history['acc'], '-') #Plot Accuracy Curve
plt.plot(history.history['val_acc'], ':')
plt.title('Model Accuracy U6')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training Set', 'Test Set'], loc='lower right')
plt.show()
