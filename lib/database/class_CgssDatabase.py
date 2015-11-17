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
from pymongo import ASCENDING


class CgssDatabase(Database):

    '''CgssDatabase类用来处理cgss数据
    '''

    def __init__(self):
        Database.__init__(self)
        self.connect('microDB', 'Cgss')

    def find(self, **conds):
        pass

if __name__ == '__main__':
    pass
