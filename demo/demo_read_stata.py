# coding=UTF-8

import pandas as pd
import numpy as np

# 读入stata文件
df = pd.read_stata('e:/Data/micro/CGSS2005_new.dta',encoding='GBK',convert_categoricals =False, iterator=True)

# 变量
variable_label = df.variable_labels()
print(len(df.lbllist),df.lbllist)
print(len(df.varlist),df.varlist)
print(len(df.vlblist),df.vlblist)
print(len(variable_label))

variable_value_label = dict(zip(df.varlist,df.lbllist))
print(len(variable_value_label),variable_value_label)

# 数据的label
labels = df.value_labels()
new_labels = dict()
for var in labels:
    var_label = list(labels[var].items())
    label_tuple = [(np.uint(item[0]).astype(int),item[1]) for item in var_label]
    new_labels[var] = dict(label_tuple)
print(new_labels)

# 数据
#data = df.read()

variable_label_dict = dict(zip(df.varlist,df.vlblist))
variable_value_label_dict = new_labels
# query
check = 'a43a'
print(check)
print(variable_label_dict[check])
print(variable_value_label[check])
print(variable_value_label_dict[variable_value_label[check]])























