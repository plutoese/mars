# coding=UTF-8

#-----------------------------------------------
# class_CgssDatabase文件
# @class: CgssDatabase类
# @introduction: CgssDatabase类用来处理cgss数据
# @dependency: pymongo，Database类
# @author: plutoese
# @date: 2015.11.16
#------------------------------------------------

from lib.database.class_Database import Database
import re
import pandas as pd


class CgssDatabase(Database):

    """

    """

    def __init__(self, year=None):
        Database.__init__(self)
        self.connect('microDB', 'Cgss')
        self.year = int(year)

    def set_year(self, year):
        self.year = int(year)

    # 时期
    @property
    def period(self):
        return self.collection.find().distinct('year')

    # 问卷问题
    def questions(self, year=None):
        '''

        :param int,str year: 年份
        :return: 包含变量及其标签的列表
        :rtype: list
        '''
        if year is None:
            year = self.year
        if isinstance(year, (int, str)):
            result = self.collection.find_one({'year': int(year)})
            result = [[key, result[key]['label'], result[key]['serial_number']] for key in result if (
                re.match('^_id$', key) is None) and (re.match('^year$', key) is None)]
            result1 = [[item[0], item[1]]
                       for item in sorted(result, key=lambda x: x[2])]
            return result1
        else:
            print('Wanted:Str or Int. You give the type of ', type(year))
            raise TypeError

    # 返回某个变量的值
    def variable(self, variable=None, year=None, label=False):
        if year is None:
            year = self.year
        result = self.collection.find(
            {'year': int(year)}, projection={variable: 1, '_id': 0})
        if label:
            result = [record[variable]['value']['label'] for record in result]
        else:
            result = [record[variable]['value']['value'] for record in result]
        return result

    def variables(self, variables=None, year=None):
        if year is None:
            year = self.year
        #
        sample = dict()
        for var in variables:
            sample[var[0]] = self.variable(variable=var[0], label=var[1])
        result = pd.DataFrame(sample)

        return result

if __name__ == '__main__':
    cgdb = CgssDatabase(year=2013)

    #indexes = [IndexModel([("year", ASCENDING)])]
    # cgdb.create_index(indexes)

    print(cgdb.period)
    print(cgdb.questions())

    print(cgdb.variable(variable='b7f'))
    print(cgdb.variable(variable='b7f', label=True))

    print(cgdb.variables(variables=[['b7f', True], ['a512', True]]))
