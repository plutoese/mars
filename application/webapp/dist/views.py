# coding=UTF-8

import re
import uuid
from flask import Blueprint, render_template, request, url_for, jsonify, redirect, session
from webapp.dist.lib.Index.class_ProvinceStatIndex import ProvinceStatIndex
from webapp.dist.lib.Index.class_CEICindex import CEICIndex
from webapp.dist.lib.database.class_ProvinceStatisticsDatabase import ProvinceStatisticsDatabase
from webapp.dist.lib.database.class_CEICDatabase import CEICDatabase
from webapp.dist.lib.file.class_Excel import Excel
import flask.ext.login as flask_login

myapp = Blueprint('myapp', __name__)

myapp.secret_key = 'hard to guset'  # Change this!
login_manager = flask_login.LoginManager()
#login_manager.init_app(myapp)

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
        form_data = request.form
        period_chosen = form_data.getlist('period')
        region_chosen = re.split(',', form_data.getlist('hregion')[0])
        variables_chosen = form_data.getlist('variable')

        conds = {'region': region_chosen, 'year': period_chosen, 'variable': variables_chosen}
        mdata = db.find(conds)
        header = mdata['header']
        data = mdata['data']
        fdata = [header]
        fdata.extend(data)

        filename = str(uuid.uuid1()) + '.xlsx'
        session['filename'] = filename
        outfile = 'E:\\gitwork\\application\\webapp\\static\\file\\' + filename
        moutexcel = Excel(outfile)
        moutexcel.new().append(fdata, 'mysheet')
        moutexcel.close()

        return render_template("queryresult.html", header=header, data=data)
    return render_template("provincedataquery.html", period=period)


@myapp.route('/prefecturedataquery', methods=['GET', 'POST'])
@flask_login.login_required
def prefecturedataquery():
    # 设置数据
    period = range(2000, 2015)
    db = CEICDatabase()

    if request.method == 'POST':
        form_data = request.form
        period_chosen = form_data.getlist('period')
        region_chosen = re.split(',', form_data.getlist('hregion')[0])
        variables_chosen = form_data.getlist('variable')

        conds = {'region': region_chosen, 'year': period_chosen, 'variable': variables_chosen}
        mdata = db.find(conds)
        header = mdata['header']
        data = mdata['data']
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
    return render_template("prefecturedataquery.html", period=period)


@myapp.route('/exceloutput')
@flask_login.login_required
def exceloutput():
    saved_file = request.script_root + '/static/file/' + session['filename']
    return redirect(saved_file)


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
        outfile = 'E:\\gitwork\\application\\webapp\\static\\file\\' + filename
        print(url_for('myapp.index'))
        moutexcel = Excel(outfile)
        moutexcel.new().append(fdata, 'mysheet')
        moutexcel.close()
        return render_template("queryresult.html", header=header, data=data)
    return render_template("query.html", period=period)


@myapp.route('/ajaxtwo', methods=['POST', 'GET'])
def ajaxtwo():
    return render_template('ajaxtwo.html')


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
    period = range(1990, 2015)
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('hregion'))
        print(formdata.getlist('variable'))
    return render_template('jquerylearning.html', period=period)


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
