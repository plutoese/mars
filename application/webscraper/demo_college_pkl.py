# coding=UTF-8

import pickle
import re

F = open('E:/gitwork/application/webscraper/college.pkl', 'rb')
college_data = pickle.load(F)
print(college_data)
print(len(college_data))

cdata = re.split('\n',college_data)
mdata = [re.split(' ',item) for item in cdata]
print(cdata)
print(mdata)