# coding=UTF-8

from flask import Blueprint, render_template, request, url_for

myapp = Blueprint('myapp', __name__)

# 网站缺省主页
@myapp.route('/')
def index():
    return render_template("index.html")

# 登录用户首页
@myapp.route('/updatedlog')
def updatedlog():
    return render_template("updatedlog.html")

# 省级数据查询
@myapp.route('/provincedataquery',methods=['GET', 'POST'])
def provincedataquery():
    period = range(1990,2015)
    print(url_for('static', filename='css/multiple-select.css'))
    if request.method == 'POST':
        form_data = request.form
        #period_chosen = request.form['period']
        #variables_chosen = request.form['variable']
        print(form_data)
    return render_template("provincedataquery.html",period=period,regions=[['浙江','温州']],variables=['人均GDP'])