# coding=UTF-8

import scipy as sp
import matplotlib.pyplot as plt

# 0. function
def error(f,x,y):
    return sp.sum((f(x)-y)**2)

# 1. load data
File = 'd:/data/web_traffic.tsv'
raw_data = sp.genfromtxt(File,delimiter='\t')
x = raw_data[:,0]
y = raw_data[:,1]

# 2. data cleaning
print(sp.sum(sp.isnan(y)))
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

# 3. plot
plt.scatter(x,y)
plt.title('Web traffic over the last month')
plt.xlabel('Time')
plt.ylabel('Hits/hour')
plt.xticks([w*7*24 for w in range(10)],['week {}'.format(w) for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
plt.show()

# 4. ployfit
fp1, residuals, rank, sv, rcond = sp.polyfit(x,y,1,full=True)
print('Model parameters: {}'.format(fp1))









