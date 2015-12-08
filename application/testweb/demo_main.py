# coding=UTF-8

from lib.database.class_Database import Database
from flask import Flask, render_template, request, redirect, url_for, jsonify
from application.DataWarehouse.data.class_regiondata import RegionData
import json

app = Flask(__name__)

# 创建初始数据
# 导入CEIC数据
db = Database()
con = db.connect('regionDB', 'CEIC')
period = range(1990,2015)
# 创建区域数据
region_list = json.load(open('e:/gitwork/application/testweb/region_ceic.txt'))
variables = con.find().distinct('variable')
rdata = RegionData()

@app.route("/")
def index():
    project_name = u'创数据'
    company_date = u'华东理工大学商学院 2015'
    return render_template('index.html',project_name=project_name,company_date=company_date)

@app.route("/query",methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        form_data = request.form
        #period_chosen = request.form['period']
        #variables_chosen = request.form['variable']
        print(form_data)
        #print(period_chosen)
        #print(variables_chosen)
    return render_template('query.html',period=period,regions=region_list,variables=variables)

@app.route("/querytest",methods=['GET','POST'])
def querytest():
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        print(formdata.getlist('period'))
    return render_template('querytest.html',period=period)

@app.route("/querytwo",methods=['GET','POST'])
def querytwo():
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        period_chosen = formdata.getlist('period')
        region_chosen = formdata.getlist('region')
        variables_chosen = formdata.getlist('variable')
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('region'))
        print(formdata.getlist('variable'))
        period_chosen = [int(y) for y in period_chosen]
        mdata = rdata.query(region=region_chosen,variable=variables_chosen,year=period_chosen)
        file = 'E:/gitwork/application/testweb/static/file/result.xlsx'
        mdata['data'].to_excel(file)
        return redirect('/static/file/result.xlsx')
    return render_template('querytwo.html',period=period,regions=region_list,variables=variables)

@app.route("/queryfour",methods=['GET','POST'])
def queryfour():
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        period_chosen = formdata.getlist('period')
        region_chosen = formdata.getlist('region')
        variables_chosen = formdata.getlist('variable')
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('region'))
        print(formdata.getlist('variable'))
        period_chosen = [int(y) for y in period_chosen]
        mdata = rdata.query(region=region_chosen,variable=variables_chosen,year=period_chosen)
        file = 'E:/gitwork/application/testweb/static/file/result.xlsx'
        mdata['data'].to_excel(file)
        return redirect('/static/file/result.xlsx')
    return render_template('queryfour.html',period=period,regions=region_list,variables=variables)

@app.route("/queryfive",methods=['GET','POST'])
def queryfive():
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        period_chosen = formdata.getlist('period')
        region_chosen = formdata.getlist('region')
        variables_chosen = formdata.getlist('variable')
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('region'))
        print(formdata.getlist('variable'))
        period_chosen = [int(y) for y in period_chosen]
    return render_template('queryfive.html',period=period,regions=region_list,variables=variables)

@app.route("/queryone",methods=['POST', 'GET'])
def queryone():
    return render_template('queryone.html')

@app.route("/about")
def about():
    return render_template('jsone.html')

@app.route("/jsdemo")
def jsdemo():
    return render_template('jsdemo.html')

@app.route("/jqueryone")
def jqueryone():
    return render_template('jqueryone.html')

@app.route("/jquerytwo")
def jquerytwo():
    return render_template('jquerytwo.html')

@app.route("/bdmap")
def bdmap():
    return render_template('bdmap.html')

@app.route("/plotly")
def plotly():
    return render_template('plotly.html')

@app.route('/ajaxone', methods=['POST', 'GET'])
def ajaxone():
    return render_template('ajaxone.html')

@app.route('/newvars')
def newvars():
    period_change = request.args.get('mperiod')
    print('nanjing')
    print(period_change)
    return jsonify(result='not good')

@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route("/form", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        return render_template('testweb.html',mname=name)
        #return redirect(url_for('login',mname=name))
    return render_template('testweb.html')


if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)