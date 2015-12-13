# coding=UTF-8

import application.machinelearning.demo.kNN as KNN
from sklearn.neighbors import KNeighborsClassifier

group, labels = KNN.createDataSet()
print(KNN.classify0([0,0],group,labels,3))
print(group)
print(labels)

neigh = KNeighborsClassifier(3)
neigh.fit(group,labels)
print(neigh.predict([0,0]))
