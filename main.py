import warnings
import csv
import math
import numpy as np
import time

from helper_functions import folds, output_vector
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

output_vector_collection = []
for i in (mlb_pit, mlb_bat, npb_pit):
    if i is mlb_pit:
        name_data = ("MLB Pitchers dataset:")
    elif i is mlb_bat:
        name_data = ("MLB Batters dataset:")
    else:
        name_data = ("NPB Pitchers dataset:")
    print(name_data)
    
    output_vectors = []
    # Decision Tree
    for j in ("gini", "entropy"):
        with MyTimer():
            confusion = folds(*i, num_folds, tree.DecisionTreeClassifier(criterion = j, random_state=0 ))
            print(confusion)
            ov = output_vector(confusion)
            print("The accuracy of Tree classifier with {} criterion is {} ".format(j,ov[4]))
            print("The F1-score of Tree classifier with {} criterion is {} ".format(j,ov[7]))
            output_vectors.append(ov)
    
    # K Nearest Neighbours
    for j in ("uniform","distance"):
        for k in range(1,16):
            with MyTimer():
                
                confusion = folds(*i, num_folds, neighbors.KNeighborsClassifier(k, weights=j))
                print(confusion)
                ov = output_vector(confusion)
                print("The accuracy of K Neighbours classifier with {} weights and k = {} is {} ".format(j,k,ov[4]))
                print("The F1-score of K Neighbours classifier with {} weights and k = {} is {} ".format(j,k,ov[7]))
                output_vectors.append(ov)

    # Support Vector Machine
    for j in ("linear", "poly", "rbf", "sigmoid"):
        with MyTimer():
            print("The accuracy of SVM classifier with {} kernel is {} ".format(j,))

            confusion = folds(*i, num_folds, svm.SVC(kernel = j, gamma = "scale"))
            print(confusion)
            ov = output_vector(confusion)
            print("The accuracy of SVM classifier with {} kernel is {} ".format(j,ov[4]))
            print("The F1-score of SVM classifier with {} kernel is {} ".format(j,ov[7]))
            output_vectors.append(ov)
    
    # ANN
    for j in ("identity", "logistic", "relu"):
        for k in range(10,101,10):
            with MyTimer():
                confusion = folds(*i, num_folds, neural_network.MLPClassifier(hidden_layer_sizes=(k,),activation=j))
                print(confusion)
                ov = output_vector(confusion)
                print("The accuracy of Multilayer Preceptron classifier with one hidden layer, {} hidden neurons, and {} activation is {} ".format(k,j,ov[4]))
                print("The F1-score of Multilayer Preceptron classifier with one hidden layer, {} hidden neurons, and {} activation is {} ".format(k,j,ov[7]))
                output_vectors.append(ov)
                
            with MyTimer():
                confusion = folds(*i, num_folds, neural_network.MLPClassifier(hidden_layer_sizes=(k,k,),activation=j))
                print(confusion)
                ov = output_vector(confusion)
                print("The accuracy of Multilayer Preceptron classifier with one hidden layer, {} hidden neurons, and {} activation is {} ".format(k,j,ov[4]))
                print("The F1-score of Multilayer Preceptron classifier with one hidden layer, {} hidden neurons, and {} activation is {} ".format(k,j,ov[7]))
                output_vectors.append(ov)
    print(" ")
    output_vector_collection.append( (name_data, output_vectors) )

for x in output_vector_collection:
    print(x[0])
    for y in x[1]:
        for z in y:
            print("{},".format(y), end = "")
        print(x[1][-1])
    print("\n")

