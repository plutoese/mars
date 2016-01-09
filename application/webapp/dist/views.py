# coding=UTF-8

import re
import uuid
import os
from flask import Blueprint, render_template, request, url_for, jsonify, redirect, session
from webapp.dist.lib.Index.class_ProvinceStatIndex import ProvinceStatIndex
from webapp.dist.lib.Index.class_CEICindex import CEICIndex
from webapp.dist.lib.database.class_ProvinceStatisticsDatabase import ProvinceStatisticsDatabase
from webapp.dist.lib.database.class_CEICDatabase import CEICDatabase
from webapp.dist.lib.file.class_Excel import Excel
from webapp.dist.lib.database.class_AQIDatabase import AQIDatabase
import flask.ext.login as flask_login
from webapp.dist.models import TEMP_FILE_FOLDER, allowed_file, RegionQueryAndSave, UPLOAD_FOLDER
from webapp.dist.models import make_upload_file_name, UploadFile
from werkzeug.utils import secure_filename

myapp = Blueprint('myapp', __name__)

myapp.secret_key = 'hard to guset'  # Change this!
login_manager = flask_login.LoginManager()


# user data
users = {'ecust': {'password': 'ecust'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(userid):
    if userid not in users:
        return

    user = User()
    user.id = userid
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user


@myapp.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


# 网站缺省主页
@myapp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    username = request.form['username']
    if username not in users:
        return "no such user"
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('myapp.updatedlog'))
    return 'Bad login'


# 登录用户首页
@myapp.route('/updatedlog')
@flask_login.login_required
def updatedlog():
    return render_template("updatedlog.html")


# 省级数据查询
@myapp.route('/provincedataquery', methods=['GET', 'POST'])
@flask_login.login_required
def provincedataquery():
    # 设置数据
    period = range(1978, 2014)
    db = ProvinceStatisticsDatabase()

    if request.method == 'POST':
        conds = {'region': re.split(',', request.form.getlist('hregion')[0]),
                 'year': request.form.getlist('period'),
                 'variable': request.form.getlist('variable')}

        region_query = RegionQueryAndSave(db, conds)
        mdata = region_query.data
        filename = region_query.save_temp_file()
        session['filename'] = filename
        return render_template("queryresult.html", header=mdata.get('header'), data=mdata.get('data'))
    return render_template("provincedataquery.html", period=period)


# 地级数据查询
@myapp.route('/prefecturedataquery', methods=['GET', 'POST'])
@flask_login.login_required
def prefecturedataquery():
    # 设置数据
    period = range(2000, 2015)
    db = CEICDatabase()

    if request.method == 'POST':
        conds = {'region': re.split(',', request.form.getlist('hregion')[0]),
                 'year': request.form.getlist('period'),
                 'variable': request.form.getlist('variable')}

        region_query = RegionQueryAndSave(db, conds)
        mdata = region_query.data
        filename = region_query.save_temp_file()
        session['filename'] = filename
        return render_template("queryresult.html", header=mdata.get('header'), data=mdata.get('data'))
    return render_template("prefecturedataquery.html", period=period)


# Excel文件下载
@myapp.route('/exceloutput')
@flask_login.login_required
def exceloutput():
    if session['filename'] is not None:
        saved_file = request.script_root + '/static/file/' + session['filename']
        return redirect(saved_file)
    return render_template("queryresult.html")


@myapp.route('/fileupload', methods=['POST', 'GET'])
@flask_login.login_required
def fileupload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = make_upload_file_name(secure_filename(file.filename),
                                             request.form['dataset_name'],
                                             request.form['dataset_uploader'])
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template('fileupload.html', status="文件上传成功")
    return render_template('fileupload.html')


@myapp.route('/userdata', methods=['POST', 'GET'])
@flask_login.login_required
def userdata():
    up_file = UploadFile()
    mdata = up_file.names_and_authors_and_linkes
    if request.method == 'POST':
        mdata = up_file.get_excel_data(request.form.get('file'))
        session['filename'] = mdata.get('filename')
        return render_template("queryresult.html", header=mdata.get('header'), data=mdata.get('data'))
    return render_template('userdata.html',data=mdata)


# 省级数据查询
@myapp.route('/query', methods=['GET', 'POST'])
def query():
    # 设置数据
    period = range(1978, 2014)
    db = ProvinceStatisticsDatabase()
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        period_chosen = form_data.getlist('period')
        region_chosen = re.split(',', form_data.getlist('hregion')[0])
        variables_chosen = form_data.getlist('variable')
        print(period_chosen)
        print(region_chosen)
        print(variables_chosen)
        conds = {'region': region_chosen, 'year': period_chosen, 'variable': variables_chosen}
        mdata = db.find(conds)
        header = mdata['header']
        data = mdata['data']
        print(mdata)
        fdata = [header]
        fdata.extend(data)
        print(fdata)
        filename = str(uuid.uuid1()) + '.xlsx'
        session['filename'] = filename
        outfile = ''.join([TEMP_FILE_FOLDER, filename])
        print(url_for('myapp.index'))
        moutexcel = Excel(outfile)
        moutexcel.new().append(fdata, 'mysheet')
        moutexcel.close()
        return render_template("queryresult.html", header=header, data=data)
    return render_template("query.html", period=period)


# 空气质量指数数据
@myapp.route('/aqiquery', methods=['POST', 'GET'])
@flask_login.login_required
def aqiquery():
    db = AQIDatabase()

    if request.method == 'POST':
        conds = {'region': request.form.getlist('city'),
                 'sdate': request.form.get('startpick'),
                 'edate': request.form.get('endpick')}

        region_query = RegionQueryAndSave(db, conds)
        mdata = region_query.data
        filename = region_query.save_temp_file()
        session['filename'] = filename
        return render_template("queryresult.html", header=mdata.get('header'), data=mdata.get('data'))
    return render_template('aqiquery.html', cities=db.city)


@myapp.route('/ajaxtwo', methods=['POST', 'GET'])
def ajaxtwo():
    db = AQIDatabase()

    if request.method == 'POST':
        form_data = request.form
        cities = form_data.getlist('city')
        start_date = form_data.get('startpick')
        end_date = form_data.get('endpick')
        conds = {'region': cities, 'sdate': start_date, 'edate': end_date}
        mdata = db.find(conds)
        header = mdata['header']
        data = mdata['data']
        print(mdata)
        fdata = [header]
        fdata.extend(data)
        print(fdata)
        filename = str(uuid.uuid1()) + '.xlsx'
        session['filename'] = filename
        outfile = 'E:\\gitwork\\application\\webapp\\static\\file\\' + filename
        moutexcel = Excel(outfile)
        moutexcel.new().append(fdata, 'mysheet')
        moutexcel.close()
        return render_template("queryresult.html", header=header, data=data)
    return render_template('ajaxtwo.html', cities=db.city)


@myapp.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    # result = a + b
    return jsonify(result=a + b)


@myapp.route('/ajaxtest', methods=['POST', 'GET'])
def ajaxtest():
    # 设置数据
    period = range(1990, 2015)
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        period_chosen = formdata.getlist('period')
        region_chosen = formdata.getlist('hregion')
        variables_chosen = formdata.getlist('variable')
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('region'))
        print(formdata.getlist('variable'))
    return render_template('ajaxtest.html', period=period)


@myapp.route('/jquerylearning', methods=['POST', 'GET'])
def jquerylearning():
    up_file = UploadFile()
    mdata = up_file.names_and_authors_and_linkes
    if request.method == 'POST':
        mdata = up_file.get_excel_data(request.form.get('file'))
        print(mdata)
        return render_template("queryresult.html", header=mdata.get('header'), data=mdata.get('data'))
    return render_template('jquerylearning.html',data=mdata)


@myapp.route('/_from_year_get_regions', methods=['POST', 'GET'])
def from_year_get_regions():
    period_done = request.values.getlist('period_done[]')
    # 这里要调用函数，通过时期获取变量
    region_generated = ProvinceStatIndex().get_regions_by_years(period_done)
    return jsonify(regions=region_generated)


@myapp.route('/_from_region_get_variables', methods=['POST', 'GET'])
def from_region_get_variables():
    regions = request.values.getlist('region_selected[]')
    years = request.values.getlist('period_selected[]')
    # 这里要调用函数，通过时期和区域获得变量
    variable_generated = ProvinceStatisticsDatabase().get_variables_from_period_regions(years, regions)
    return jsonify(variables=variable_generated)


@myapp.route('/_prefeture_from_year_get_regions', methods=['POST', 'GET'])
def prefeture_from_year_get_regions():
    period_done = request.values.getlist('period_done[]')
    print(period_done)
    # 这里要调用函数，通过时期获取变量
    region_generated = CEICIndex().get_regions_by_years(period_done)
    return jsonify(regions=region_generated)


@myapp.route('/_prefeture_from_region_get_variables', methods=['POST', 'GET'])
def prefeture_from_region_get_variables():
    regions = request.values.getlist('region_selected[]')
    years = request.values.getlist('period_selected[]')
    # 这里要调用函数，通过时期和区域获得变量
    variable_generated = CEICDatabase().get_variables_from_period_regions(years, regions)
    return jsonify(variables=variable_generated)
