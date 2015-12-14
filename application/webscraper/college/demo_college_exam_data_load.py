# coding=UTF-8

import pickle

file = 'E:/Data/college/c5.pkl'
F = open(file, 'rb')
college_data = pickle.load(F)
print(college_data)
