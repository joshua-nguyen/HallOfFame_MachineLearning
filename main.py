import warnings
import csv
import math
import numpy as np
import time

from sklearn import tree
from sklearn import neighbors
from sklearn import svm
from sklearn import neural_network

class MyTimer():
 
    def __init__(self):
        self.start = time.time()
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete'
        print(msg.format(time=runtime))


def warn(*args, **kwargs):
    pass
warnings.warn = warn

def folds(data_set, start_column, end_column, target_column, num_folds, model):
    fold_classification_total = 0
    for fold in range(num_folds):
        chunk = math.floor(len(data_set)/num_folds)
        start = fold*chunk
        end = start+chunk

        data = np.copy(data_set[:,start_column:end_column])
        data = data.astype(float)
        target = np.copy(data_set[:,target_column])
        train_data = np.delete(data, np.s_[start:end], axis = 0)
        test_data = data[start:end]
        train_target = np.delete(target, np.s_[start:end], axis = 0)
        test_target = target[start:end]
        model.fit(train_data, train_target)

        subtotal = 0
        for i in range(end-start):
            if model.predict([test_data[i]]) == test_target[i]:
                subtotal += 1
        fold_mean = subtotal / chunk
        fold_classification_total += fold_mean
    return fold_classification_total / num_folds


"""aardsda01,2004,1,SFN,NL,1,0,11,0,0,0,0,32,20,8,1,10,5,0.417,6.75,0,0,2,0,61,5,8,0,1,1,0"""
a=[]
with open("mlb_pitch_cumul_target.csv","r") as f:
    b = csv.reader(f, delimiter = ',')
    for i in b:
        a.append(i)
mlb_pitchers = np.asarray(a,dtype=None,order=None)

mlb_pit = (mlb_pitchers, 5, 30, 30)


"""abercda01,1871,1,TRO,NA,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"""
a=[]
with open("mlb_bat_cumul_target.csv","r") as f:
    b = csv.reader(f, delimiter = ',')
    for i in b:
        a.append(i)
mlb_batters = np.asarray(a,dtype=None,order=None)
mlb_bat = (mlb_batters, 5, 22, 22)

"""abbotky01,1994,1,KIN,AL,0,0,4,4,0,0,0,35,25,10,0,9,8,0,7.71,0,0,0,0,65,0,11,0"""
a=[]
with open("npb_pitch_cumul_target.csv","r") as f:
    b = csv.reader(f, delimiter = ',')
    for i in b:
        a.append(i)
npb_pitchers = np.asarray(a,dtype=None,order=None)
npb_pit = (npb_pitchers, 5, 27, 27)

num_folds = 10

for i in (mlb_pit, mlb_bat, npb_pit):
    if i is mlb_pit:
        print ("MLB Pitchers dataset:")
    elif i is mlb_bat:
        print ("MLB Batters dataset:")
    else:
        print ("NPB Pitchers dataset:")
    
    for j in ("gini", "entropy"):
        with MyTimer():
            print("The accuracy of Tree classifier with {} criterion is {} ".format(j,folds(*i, num_folds, tree.DecisionTreeClassifier(criterion = j, random_state=0 ))))
    for j in ("uniform","distance"):
        for k in range(1,16):
            with MyTimer():
                print("The accuracy of K Neighbours classifier with {} weights and k = {} is {} ".format(j,k,folds(*i, num_folds, neighbors.KNeighborsClassifier(k, weights=j))))
    for j in ("linear", "poly", "rbf", "sigmoid"):
        with MyTimer():
            print("The accuracy of SVM classifier with {} kernel is {} ".format(j,folds(*i, num_folds, svm.SVC(kernel = j, gamma = "scale"))))
    for j in ("identity", "logistic", "tanh", "relu"):
        for k in range(10,101,10):
            with MyTimer():
                print("The accuracy of Multilayer Preceptron classifier with one hidden layer, {} hidden neurons, and {} activation is {} ".format(k,j,folds(*i, num_folds, neural_network.MLPClassifier(hidden_layer_sizes=(k,),activation=j))))
            with MyTimer():
                print("The accuracy of Multilayer Preceptron classifier with two hidden layer, {} hidden neurons on each layer, and {} activation is {} ".format(k,j,folds(*i, num_folds, neural_network.MLPClassifier(hidden_layer_sizes=(k,k,),activation=j))))
    print(" ")
