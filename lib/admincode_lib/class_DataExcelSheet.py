# coding=UTF-8

#--------------------------------------------------------
# class_DataExcelSheet文件
# @class: DataExcelSheet类
# @introduction: DataExcelSheet类用来处理Excel格式的原始数据
# @dependency: pandas，Database类
# @author: plutoese
# @date: 2015.11.16
#--------------------------------------------------------

from lib.file.class_Excel import Excel
import pandas as pd

# 处理DataExcelSheet的主类，用来被继承。
# 可以导出DataSet类，有序字典格式
class DataExcelSheet:
    '''
    类DataExcelSheet是数据表单的主类，用以被继承。
    
    属性：
    rawdata: 原始数据
    '''

    def __init__(self, filename=None,sheet=0,type=None):
        if type is None:
            self.rawdata = Excel(filename).read(sheet=sheet)
        else:
            self.rawdata = pd.read_excel(filename,sheet)

if __name__ == '__main__':
    mdatasheet = DataExcelSheet('e:/data/admincode/admin_code_1990_1992.xlsx',sheet=0)
    print(mdatasheet.rawdata)