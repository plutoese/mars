# coding=UTF-8

import rpy2.robjects as robjects

pi = robjects.r['pi']
print(pi[0])
