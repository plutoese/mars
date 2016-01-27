# coding=UTF-8

# --------------------------------------------------------------------------------
# models文件
# @introduction: 初始化变量，函数和类
# @dependency: None
# @author: plutoese
# @date: 2016.01.08
# ---------------------------------------------------------------------------------

import uuid, os, datetime, re
import pandas as pd
import numpy as np
from webapp.dist.lib.file.class_Excel import Excel
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.charts import Bar, Scatter, output_file, show
from bokeh.models import PrintfTickFormatter, DatetimeTickFormatter

TEMP_FILE_FOLDER = 'E:/gitwork/application/webapp/static/file/'
UPLOAD_FOLDER = 'E:/gitwork/application/webapp/static/file/uploads/'
# upload file restriction
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])
TODAY = datetime.date.today().strftime('%Y-%m-%d')
COLOR = ['#DC143C','#006400','#9400D3','#1E90FF','DAA520','CD5C5C','FFC0CB']


class RegionQueryAndSave:
    """类RegionQuery用来执行区域数据查询，返回查询得到的数据

    """

    def __init__(self, database, conds):
        self.db = database
        self.conds = conds
        self.excel_data = None

    @property
    def data(self):
        self.query_data = self.db.find(self.conds)

        if self.query_data is None:
            return {'header': [], 'data': [[]]}

        header = self.query_data.get('header', [])
        data = self.query_data.get('data', [[]])

        self.excel_data = [header]
        self.excel_data.extend(data)

        return {'header': header, 'data': data}

    def save_temp_file(self):
        """ 储存临时文件

        :return:
        """
        if self.excel_data is not None:
            filename = str(uuid.uuid1()) + '.xlsx'
            tmp_filepath = ''.join([TEMP_FILE_FOLDER, TODAY])
            if not os.path.isdir(tmp_filepath):
                os.mkdir(tmp_filepath)

            outfile = ''.join([tmp_filepath, '/', filename])
            moutexcel = Excel(outfile)
            moutexcel.new().append(self.excel_data, 'mysheet')
            moutexcel.close()

            return ''.join([TODAY, '/', filename])
        return None


class UploadFile():
    def __init__(self, filepath=UPLOAD_FOLDER):
        self.file_path = filepath

    @property
    def files(self):
        return os.listdir(self.file_path)

    @property
    def names_and_authors_and_linkes(self):
        result = []
        for file in self.files:
            item = re.split('_', file)
            result.append([item[0], item[1], ''.join([self.file_path, file])])
            #result.append([item[0], item[1], ''.join([self.file_path, '/', file])])
        return result

    def get_excel_data(self,filename):
        mexcel = Excel(filename)
        mdata = mexcel.read()
        header = mdata.pop(0)
        return {'header':header,'data':mdata,'filename':re.split(TEMP_FILE_FOLDER,filename)[1]}


# 载入储存的数据文件
class LoadData():
    def __init__(self,filename):
        self.filename = filename

    def load(self):
        mexcel = Excel(self.filename)
        self._data = mexcel.read()
        # 生成数据集变量集合对应的字典
        head = self._data.pop(0)
        header = {''.join(['v','{:03d}'.format(i)]):head[i] for i in range(len(head))}
        anti_header = {head[i]:''.join(['v','{:03d}'.format(i)]) for i in range(len(head))}
        return {'header':header,'anti_header':anti_header,'data':pd.DataFrame(self._data,columns=sorted(header.keys()))}


# Bokeh动态统计图表库
class BokehGraph():
    def __init__(self,load_data):
        self._data = load_data['data']
        self._header = load_data['header']
        self.anti_header = load_data['anti_header']

    # 折线图，其中group是字典形式
    def line_plot(self,xvar,yvar,group=None,timeseries=False):
        m_xvar = self.anti_header.get(xvar)
        m_yvar = self.anti_header.get(yvar)
        p = figure()
        if group is None:
            mdata_dict = self._data.to_dict('list')
            if timeseries:
                dates = np.array(mdata_dict[m_xvar],dtype=np.datetime64)
                p.line(dates,mdata_dict[m_yvar],alpha=0.5)
                p.xaxis[0].formatter = DatetimeTickFormatter()
            else:
                p.circle(mdata_dict[m_xvar],mdata_dict[m_yvar])
                p.line(mdata_dict[m_xvar],mdata_dict[m_yvar])
        else:
            group_var = self.anti_header.get(group)
            i = 0
            for g in self._data[group_var].drop_duplicates():
                mdata = self._data[self._data[group_var]==g]
                mdata_dict = mdata.to_dict('list')
                if timeseries:
                    dates = np.array(mdata_dict[m_xvar],dtype=np.datetime64)
                    p.line(dates,mdata_dict[m_yvar],alpha=0.5,legend=g,line_color=COLOR[i])
                    p.xaxis[0].formatter = DatetimeTickFormatter()
                else:
                    p.circle(mdata_dict[m_xvar],mdata_dict[m_yvar])
                    p.line(mdata_dict[m_xvar],mdata_dict[m_yvar],line_color=COLOR[i],legend=g)
                i += 1
        #output_file('bar.html')
        #show(p)
        script, div = components(p)
        return {'script':script, 'div':div}

    # 条形图
    def bar_plot(self,var,label):
        m_var = self.anti_header.get(var)
        m_label = self.anti_header.get(label)
        p = Bar(self._data, m_label, values=m_var, agg='mean', title='条形图', xlabel=label, ylabel=var)
        script, div = components(p)
        return {'script':script, 'div':div}

    # 散点图
    def scatter(self,xvar,yvar,group=None):
        m_xvar = self.anti_header.get(xvar)
        m_yvar = self.anti_header.get(yvar)
        if group is None:
            p = Scatter(self._data, x=m_xvar, y=m_yvar, title='散点图', xlabel=xvar, ylabel=yvar)
        else:
            m_group = self.anti_header.get(group)
            p = Scatter(self._data, x=m_xvar, y=m_yvar, color=m_group,
                        title='散点图', legend="top_left",
                        xlabel=xvar, ylabel=yvar)
        #output_file('bar.html')
        #show(p)
        script, div = components(p)
        return {'script':script, 'div':div}


# 上传文件后缀检验
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def make_upload_file_name(file, name, author):
    file_type = file.rsplit('.', 1)[1]
    random_part = str(uuid.uuid1())
    return ''.join([name, '_', author, '_', random_part, '.', file_type])


if __name__ == '__main__':
    print(make_upload_file_name('demo.xls', '城市数据', 'glen'))

    up_file = UploadFile()
    print(up_file.files)
    print(up_file.names_and_authors_and_linkes)

    file = 'E:/gitwork/application/webapp/static/file/uploads/医院数据_glen_314542d8-b685-11e5-bf35-f582ef2c4802.xls'
    print(up_file.get_excel_data(file).get('header'))
    print(up_file.get_excel_data(file).get('data'))

    file = 'd:/temp/airquality.xlsx'
    ldata = LoadData(file)
    print(ldata.load())

    bgraph = BokehGraph(ldata.load())
    #bgraph.bar_plot('AQI指数','city')
    #bgraph.scatter('PM10','PM25','city')

    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    mdata = bgraph.line_plot(xvar='日期',yvar='AQI指数',group='city',timeseries=True)
    print(mdata['div'])
    print(mdata['script'])
