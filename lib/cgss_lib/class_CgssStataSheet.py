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
import pandas as pd
from datetime import datetime
from lib.file.class_Stata import Stata
from lib.database.class_CgssDatabase import CgssDatabase
from lib.file.class_Excel import Excel


class CgssStataSheet:

    '''类CgssStataSheet用来读写cgss.dta（stata格式）的数据文件

    :param str filename: 想要读写的文件名
    :param int year: 年份
    :param str encoding: 编码方式，默认是'GBK'
    :return: 无返回值
    :var list variables: 变量列表
    :var list variables_labels: 变量标签列表
    :var list variables_values_labels: 变量的值标签
    :var list values_labels: 值标签的内容
    :var dict variables_labels_dict: 变量-标签字典
    :var dict variables_values_labels_dict: 变量-值标签字典
    :var dict values_labels_dict: 值-标签字典
    '''

    def __init__(self, filename, year=2013, encoding='GBK'):
        self.cgss_db = CgssDatabase()

        self.stata_object = Stata(filename, encoding=encoding)
        self.stata_file = self.stata_object.stata_file

        self.year = int(year)

        # 变量-标签字典
        self.variables_labels_dict = dict(
            zip(self.stata_object.variables, self.stata_object.variables_labels))
        # 变量-值标签字典
        self.variables_values_labels_dict = dict(
            zip(self.stata_object.variables, self.stata_object.variables_values_labels))
        # 值标签字典
        self.values_labels_dict = self.values_labels

    def insert(self):
        '''insert方法用来插入数据到Mongodb数据库集合
        '''
        # 读入stata文件数据
        data = self.stata_object.read()
        # 数据行数
        data_rows = data.shape[0]
        print(data_rows)

        # 读取每一行数据（产生一条记录）
        for i in range(data_rows):
            # 每一条记录用字典记录，存储在record变量中
            record = dict({'year': self.year})
            # 读取一条记录
            row_data = data.iloc[i]
            # 包装记录，即记录变量数据在字典record中
            # ind是行数据的索引（即变量）
            for ind in row_data.index:
                # 初始化值标签
                value_label = None
                # 变量-值标签变量
                variable_value_labels = self.variables_values_labels_dict[ind]
                # 值标签字典
                value_labels = self.values_labels_dict.get(
                    variable_value_labels, None)
                # 变量的值
                value = row_data[ind]

                # 如果变量的值是数值型
                if isinstance(value, (np.float32, np.float64, np.integer)):
                    if np.isnan(value):
                        value = None
                    else:
                        if value_labels is None:
                            value = None
                        else:
                            if np.equal(value, np.int(value)):
                                value = int(value)
                                value_label = value_labels.get(
                                    np.int(value), None)
                            else:
                                value = float(value)
                elif isinstance(value, str):
                    if re.match('^\s*$', value) is not None:
                        value = None
                elif isinstance(value, (pd.tslib.Timestamp, datetime)):
                    if isinstance(value, pd.tslib.NaTType):
                        value = None
                    else:
                        value = re.split(' ', str(value))[0]
                else:
                    print(ind)
                    print(value, type(value))
                    raise TypeError
                record[ind] = {'label': self.variables_labels_dict[ind],
                               'value': {
                                   'value': value,
                                   'label': value_label
                }}
            print(i)
            print('record', record)
            self.cgss_db.collection.insert(record)

    @property
    def values_labels(self):
        labels = self.stata_object.values_labels
        new_labels_dict = dict()
        for var in labels:
            var_label = list(labels[var].items())
            label_tuple = [(np.uint(item[0]).astype(int), item[1])
                           for item in var_label]
            new_labels_dict[var] = dict(label_tuple)
        return new_labels_dict


if __name__ == '__main__':
    filename = "E:/Data/micro/cgss2013.dta"
    st = CgssStataSheet(filename)
    print(st.stata_file)
    print(st.variables_labels_dict)
    print(st.variables_values_labels_dict)
    st.insert()

    '''result = st.cgss_db.collection.find_one()
    mdata = list()
    for var in st.stata_object.variables:
        mdata.append([var,result[var]['label'],result[var]['value']['value'],result[var]['value']['label']])
    print(mdata)

    outfile = 'd:/down/cgss_demo1.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new().append(mdata,'mysheet')
    moutexcel.close()'''
