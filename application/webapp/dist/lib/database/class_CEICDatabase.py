# coding=UTF-8

#-----------------------------------------------
# class_CEICDatabase文件
# @class: CEICDatabase类
# @introduction:CEICDatabase类连接CEIC数据库集合进行操作
# @dependency: pymongo
# @author: plutoese
# @date: 2016.01.03
#------------------------------------------------
"""
.. code-block:: python

    db = CEICDatabase()
    period = db.period
"""

from webapp.dist.lib.database.class_Database import Database

class CEICDatabase(Database):
    """ CEICDatabase类连接CEIC数据库集合库进行操作
    """
    def __init__(self):
        Database.__init__(self)
        self.connect('regionDB', 'CEIC')

    def get_region_by_year(self,year):
        """ 获得某年的可选择的区域

        :param int year: 年份
        :return: 区域字典
        :rtype: dict
        """
        region_acode = sorted(self.collection.find({'year':year}).distinct('acode'))
        region_recode = [self.collection.find_one({'year':year,'acode':acode}) for acode in region_acode]
        region_dict = {item['acode']:item['region'] for item in region_recode}
        return region_dict

    @property
    def period(self):
        return sorted(self.collection.find().distinct('year'))

    @property
    def variable(self):
        return sorted(self.collection.find().distinct('variable'))


if __name__ == '__main__':
    db = CEICDatabase()
    period = db.period
    print(db.collection)
    print(period)
    print(db.variable)

    indexdb = Database()
    indexcollection = indexdb.connect('indexDB','CEIC_region')
    print(indexcollection)
    for year in period:
        region_record = db.get_region_by_year(year)
        region_record['year'] = year
        indexcollection.insert(region_record)
