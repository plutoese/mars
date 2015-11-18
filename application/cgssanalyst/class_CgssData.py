# coding=UTF-8

#-----------------------------------------------
# class_CgssData文件
# @class: CgssData类
# @introduction: CgssData类用来获取cgss数据
# @dependency: pymongo，Database类
# @author: plutoese
# @date: 2015.11.17
#------------------------------------------------

from lib.database.class_CgssDatabase import CgssDatabase

class CgssData:
    def __init__(self):
        # 连接Cgss数据库
        self.cgss_database = CgssDatabase()
        self.con = self.cgss_database.collection

    def questions(self,year=None):
        record = self.con.find_one({'year':year})

        return record


if __name__ == '__main__':
    cgss_data = CgssData()
    print(cgss_data.questions(2005))

