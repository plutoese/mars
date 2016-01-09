# coding=UTF-8

# --------------------------------------------------------------------------------
# models文件
# @introduction: 初始化变量，函数和类
# @dependency: None
# @author: plutoese
# @date: 2016.01.08
# ---------------------------------------------------------------------------------

import uuid, os, datetime, re
from webapp.dist.lib.file.class_Excel import Excel

TEMP_FILE_FOLDER = 'E:/gitwork/application/webapp/static/file/'
UPLOAD_FOLDER = 'E:/gitwork/application/webapp/static/file/uploads'
# upload file restriction
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])
TODAY = datetime.date.today().strftime('%Y-%m-%d')


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
            result.append([item[0], item[1], ''.join([self.file_path, '/', file])])
        return result

    def get_excel_data(self,filename):
        mexcel = Excel(filename)
        mdata = mexcel.read()
        header = mdata.pop(0)
        return {'header':header,'data':mdata,'filename':re.split(TEMP_FILE_FOLDER,filename)[1]}


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