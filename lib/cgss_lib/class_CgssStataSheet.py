# coding=UTF-8

#------------------------------------------------------------------
# class_CgssStataSheet文件
# @class: CgssStataSheet类
# @introduction: CgssStataSheet类用来读写cgss.dta（stata格式）的数据文件
# @dependency: pymongo，numpy
# @author: plutoese
# @date: 2015.11.16
#------------------------------------------------------------------

import re
import numpy as np
from lib.file.class_Stata import Stata
from lib.database.class_CgssDatabase import CgssDatabase
from lib.file.class_Excel import Excel


class CgssStataSheet:

    def __init__(self, filename, encoding='GBK'):
        self.cgss_db = CgssDatabase()

        self.stata_object = Stata(filename, encoding=encoding)
        self.stata_file = self.stata_object.stata_file

        # 变量-标签字典
        self.variables_labels_dict = dict(
            zip(self.stata_object.variables, self.stata_object.variables_labels))
        # 变量-值标签字典
        self.variables_values_labels_dict = dict(
            zip(self.stata_object.variables, self.stata_object.variables_values_labels))

    def insert(self):
        data = self.stata_object.read()
        data_rows = data.shape[0]

        for i in range(1):
            record = dict()
            row_data = data.iloc[i]
            for ind in row_data.index:
                # 初始化
                value = None
                value_label = None
                # 变量-值标签变量
                variable_value_labels = self.variables_values_labels_dict[ind]
                # 值标签字典
                value_labels = self.values_labels_dict.get(variable_value_labels,None)

                value = row_data[ind]
                if isinstance(value,(np.float32,np.float64,np.integer)):
                    if np.isnan(value):
                        value = None
                        valeu_label = None
                    else:
                        if value_labels is None:
                            value = None
                            value_label = None
                        else:
                            if np.equal(value,np.int(value)):
                                value = np.int(value)
                                value_label = value_labels.get(np.int(value),None)
                            else:
                                value = value
                                value_label = None

                elif isinstance(value,str):
                    if re.match('^\s+$',value) is not None:
                        value = None
                        value_label = None
                else:
                    print(type(value))
                    raise TypeError
                record[ind] = {'label':self.variables_labels_dict[ind],
                               'value':{
                                   'value':value,
                                   'label':value_label
                               }}
            print('record',record)
            self.cgss_db.collection.insert(record)

    @property
    def values_labels_dict(self):
        labels = self.stata_object.values_labels
        new_labels_dict = dict()
        for var in labels:
            var_label = list(labels[var].items())
            label_tuple = [(np.uint(item[0]).astype(int), item[1])
                           for item in var_label]
            new_labels_dict[var] = dict(label_tuple)
        return new_labels_dict


if __name__ == '__main__':
    filename = "E:/Data/micro/CGSS2010.dta"
    st = CgssStataSheet(filename)
    print(st.stata_file)
    print(st.variables_labels_dict)
    print(st.variables_values_labels_dict)
    #st.insert()

    result = st.cgss_db.collection.find_one()
    mdata = list()
    for var in st.stata_object.variables:
        mdata.append([var,result[var]['label'],result[var]['value']['value'],result[var]['value']['label']])
    print(mdata)

    outfile = 'd:/down/cgss_demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new().append(mdata,'mysheet')
    moutexcel.close()
