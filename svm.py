import csv
import math
import numpy as np
from sklearn import svm
'''
aardsda01,2004,1,SFN,NL,1,0,11,0,0,0,0,32,20,8,1,10,5,0.417,6.75,0,0,2,0,61,5,8,0,1,1,0
'''

a=[]
with open("mlb_pitch_cumul_target.csv","r") as f:
    b = csv.reader(f, delimiter = ',')
    for i in b:
        a.append(i)
#print(a)
table = np.asarray(a,
dtype=None,#['U9', int, int, 'U3', 'U3',  int, int, int, int, int, int, int, int, int, int, int, int, int, float, float, int, int, int, int, int, int, int, int, int, int, int],
order=None)
X = table[:,5:29]
y = table[:,30]


fold_av=0
for fold in range(10):
    chunk = math.floor(len(table)/10)
    start = fold*chunk
    end = start+chunk-1
    #print("start {} end {}".format(start,end))
    trainX = np.copy(X)
    testX = np.delete(trainX,np.s_[start:end],axis = 0)
    #print(testX)
    #print(len(X))
    #print(len(trainX))
    #print(len(testX))
    #print(testX[0])
    trainy = np.copy(y)
    testy = np.delete(trainy,np.s_[start:end],axis =0)
    clf = svm.SVC(gamma='scale')
    clf.fit(trainX,trainy)
    subTot=0
    for i in range(chunk):
        #print(testX[i])
        if clf.predict([testX[i]])==testy[i]:
            subTot +=1
    fold_av += subTot/chunk
    print(subTot/chunk)
fold_av /= 10

print(fold_av)
