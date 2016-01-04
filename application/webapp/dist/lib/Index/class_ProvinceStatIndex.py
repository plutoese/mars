# coding=UTF-8

# ----------------------------------------------------------------
# class_ProvinceStatIndex文件
# @class: ProvinceStatIndex类
# @introduction:ProvinceStatIndex类提供ProvinceStatistics的索引服务
# @dependency: ProvinceStatisticsDatabase
# @author: plutoese
# @date: 2016.01.04
# -----------------------------------------------------------------

from webapp.dist.lib.database.class_Database import Database
from webapp.dist.lib.database.class_ProvinceStatisticsDatabase import ProvinceStatisticsDatabase


class ProvinceStatIndex:
    """ ProvinceStatIndex类提供ProvinceStatistics的索引服务
    """
    def __init__(self):
        db = Database()
        self.index_conn = db.connect('indexDB', 'ProvinceStat_region')
        self.stat_conn = ProvinceStatisticsDatabase().collection

    # 返回某年的区域列表
    def get_regions_by_year(self,year):
        record = self.index_conn.find_one({'year':int(year)})
        record.pop('_id')
        record.pop('year')
        return record

    # 返回某几年的区域列表
    def get_regions_by_years(self,years):
        record = self.get_regions_by_year(years[0])
        for y in years[1:]:
            record.update(self.get_regions_by_year(y))

        regions = []
        for acode in sorted(record):
            regions.append({'text':record[acode],'tags':[acode]})
        region_list = [{'text':'中国','tags':['000000'],'nodes':regions}]
        return region_list

    @property
    def period(self):
        return sorted(self.index_conn.find().distinct('year'))


if __name__ == '__main__':
    db = ProvinceStatIndex()
    period = db.period
    print(period)

    print(len(db.get_regions_by_year(1966)))
    print(db.get_regions_by_years(['1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']))

