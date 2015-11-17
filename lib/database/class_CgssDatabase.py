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
from pymongo import ASCENDING,IndexModel

class CgssDatabase(Database):

    '''CgssDatabase类用来处理cgss数据
    '''

    def __init__(self):
        Database.__init__(self)
        self.connect('microDB', 'Cgss')

    # 时期
    @property
    def period(self):
        return self.collection.find().distinct('year')

    # 问卷问题
    def questions(self,year=None):
        '''

        :param int,str year: 年份
        :return: 包含变量及其标签的列表
        :rtype: list
        '''
        if isinstance(year,(int,str)):
            result = self.collection.find_one({'year':int(year)})
            return [[key,result[key]['label']] for key in sorted(result) if (re.match('^_id$',key) is None) and (re.match('^year$',key) is None)]
        else:
            print('Wanted:Str or Int. You give the type of ',type(year))
            raise TypeError

if __name__ == '__main__':
    cgdb = CgssDatabase()

    #indexes = [IndexModel([("year", ASCENDING)])]
    #cgdb.create_index(indexes)

    print(cgdb.period)
    #print(cgdb.questions(2011))