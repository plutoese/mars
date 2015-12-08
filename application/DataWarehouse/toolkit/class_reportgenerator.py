# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: report
# @introduction: 类CrossSectionDataExplorer用来对横截面数据进行数据处理和探索性分析
# @property:
# @method:
# -----------------------------------------------------------------------------------------

from library.report.class_report import Report
from application.DataWarehouse.data.class_regiondata import RegionData
from application.DataWarehouse.toolkit.class_crosssectiondataexplorer import CrossSectionRegionDataExplorer


class ReportGenerator:
    '''
    类ReportGenerator是报告生成器
    '''
    # 构造函数
    def __init__(self,config):
        self.config = config



class RegionReportGenerator(ReportGenerator):
    '''
    类ReportGenerator是报告生成器
    '''
    # 构造函数
    def __init__(self,config=None):
        ReportGenerator.__init__(self,config)
        self.regionData = RegionData()
        self._setup()

    # 初始化参数
    def _setup(self):
        # 确定的参数
        self.variables = self.config['variables']
        self.reportTitle = self.config['report_title']
        self.reportPath = self.config['report_path']






if __name__ == '__main__':
    VARS = {'第一产业占GDP的比重':None,'第二产业占GDP的比重':None, '第三产业占GDP的比重':None}
    PERIOD = list(range(2010,2014))
    REPORTTITLE = u'探索性区域分析报告(Version 1)'
    REPORTAUTHOR = u'冥王星人'
    REOIRTPATH = 'E:/Report/Region_Report_first_version.pdf'
    config = {'variables':VARS,'year':PERIOD,'report_title':REPORTTITLE,'report_author':REPORTAUTHOR,'report_path':REOIRTPATH}

    generator = RegionReportGenerator(config)
    print(generator.variables.keys())
