from __future__ import absolute_import
from __future__ import print_function
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
from sklearn.preprocessing import StandardScaler as skpp
import random
import pickle

'''
    Train a simple deep NN on the MNIST dataset.

    Get to 98.40% test accuracy after 20 epochs
    (there is *a lot* of margin for parameter tuning).
    2 seconds per epoch on a K520 GPU.
'''

def reduce(x,y):
	
	z_x,z_y = [],[]
	nz_x,nz_y = [],[]

	n = len(x_train)
	for i in range(n):
		if y[i] != 0:
			nz_x.append(x[i])
			nz_y.append(y[i])
	nz_x = np.asarray(nz_x)
	nz_y = np.asarray(nz_y)
	
	m = len(nz_x)
	ratio = float(m)/(n-m)
	for i in range(n):
		if y[i] == 0:
			a = random.random()
			if a < ratio:
				z_x.append(x[i])
				z_y.append(y[i])
	z_x = np.asarray(z_x)
	z_y = np.asarray(z_y)

	res_x = np.append(z_x,nz_x,axis = 0)
	res_y = np.append(z_y,nz_y,axis = 0)

	return res_x,res_y

batch_size = 64
nb_classes = 3
nb_epoch = 500

# the data, shuffled and split between tran and test sets
# (X_train, y_train), (X_test, y_test) = mnist.load_data()

# X_train = X_train.reshape(60000, 784)
# X_test = X_test.reshape(10000, 784)
# X_train = X_train.astype("float32")
# X_test = X_test.astype("float32")
# X_train /= 255
# X_test /= 255
# print(X_train.shape[0], 'train samples')
# print(X_test.shape[0], 'test samples')

# st1 = './Feature-min/Fold1/trainingset.txt'
# st2 = './Feature-min/Fold2/trainingset.txt'
# st3 = './Feature-min/Fold3/trainingset.txt'
# st4 = './Feature-min/Fold4/trainingset.txt'
# st5 = './Feature-min/Fold4/testset.txt'

# x_train,y_train = fd.load_dataset([st1,st2,st3,st4])
# x_test,y_test = fd.load_dataset([st4])
# print (x_test.shape)

with open('modified_data_x') as f:
	x = pickle.load(f)
with open('modified_data_y') as f:
	y = pickle.load(f)
n = len(x)
m = int(n*0.8)

X_train = np.asarray(x[:m])
y_train = np.asarray(y[:m])

X_test = np.asarray(x[m:])
y_test = np.asarray(y[m:])

print (str(X_train.shape),str(X_test.shape))
# X_train = skpp().fit_transform(x_train)
# X_test = skpp().fit_transform(x_test)

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

do = 0.5
model = Sequential()
model.add(Dense(64, input_shape=(128,)))
model.add(Activation('sigmoid'))
model.add(Dropout(do))
model.add(Dense(32))
model.add(Activation('sigmoid'))
model.add(Dropout(do))
model.add(Dense(8))
model.add(Activation('sigmoid'))
model.add(Dropout(do))
model.add(Dense(3))
model.add(Activation('softmax'))

rms = RMSprop()
model.compile(loss='categorical_crossentropy', optimizer=rms)

model.fit(X_train, Y_train,
          batch_size=batch_size, nb_epoch=nb_epoch,
          show_accuracy=True, verbose=2)

x_ = X_test
y_ = model.predict_classes(x_)
res = [0,0,0]
for i in Y_test:
	if np.argmax(i) == 0:
		res[0] += 1
	elif np.argmax(i) == 1:
		res[1] += 1
	elif np.argmax(i) == 2:
		res[2] += 1
print (res)

res = [0,0,0]
for i in y_:
	if i == 0:
		res[0] += 1
	elif i == 1:
		res[1] += 1
	elif i == 2:
		res[2] += 1
print (res)

score = model.evaluate(X_test, Y_test,
                       show_accuracy=True, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])