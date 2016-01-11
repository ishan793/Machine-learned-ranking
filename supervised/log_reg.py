import numpy as np
import sklearn.linear_model as sklm
from sklearn import svm
from sklearn import datasets as ds
from sklearn.preprocessing import StandardScaler as skpp	
import pickle

import random
def try_(x,y,x_test,y_test,j):
	x_train = skpp().fit_transform(x)
	x_test = skpp().fit_transform(x_test)

	clf = svm.LinearSVC(C=j)
	clf.fit(x_train,y)

	acc = clf.score(x_test,y_test)
	print acc
	return clf.predict(x_test)


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

with open('modified_data_x') as f:
	x = pickle.load(f)
with open('modified_data_y') as f:
	y = pickle.load(f)
n = len(x)
m = int(n*0.8)

x_train = np.asarray(x[:m])
y_train = np.asarray(y[:m])

x_test = np.asarray(x[m:])
y_test = np.asarray(y[m:])

print (str(x_train.shape),str(x_test.shape))

# st1 = './Feature-min/Fold1/trainingset.txt'
# st2 = './Feature-min/Fold2/trainingset.txt'
# st3 = './Feature-min/Fold3/trainingset.txt'
# st4 = './Feature-min/Fold4/trainingset.txt'
# st5 = './Feature-min/Fold4/testset.txt'

# x_train,y_train = fd.load_dataset([st1,st2,st3,st4])
# x_test,y_test = fd.load_dataset([st4])

x_train,y_train = reduce(x_train,y_train)
ss = 0.1
k = 0.0001
for i in range(10):
	print k+ss*i
	try_(x_train,y_train,x_test,y_test,k+ss*i)
res = [0,0,0]
for i in y_test:
	res[i] += 1
print res

y_pred = try_(x_train,y_train,x_test,y_test,0.1)

res = [0,0,0]
for i in y_pred:
	res[i] += 1
print res
