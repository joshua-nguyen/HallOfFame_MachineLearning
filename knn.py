import csv
import math
import numpy as np
from sklearn.neighbors import NearestNeighbors

a=[]
with open("mlb_pitch_cumul_target.csv","r") as f:
    b = csv.reader(f, delimiter = ',')
    for i in b:
        a.append(i)
#print(a)
table = np.asarray(a,dtype= None, order=None)
X = table[:,5:29]
y = table[:,30]
print(table)
print(X)
print(y)