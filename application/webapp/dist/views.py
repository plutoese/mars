# coding=UTF-8

from flask import Blueprint, render_template, request, url_for, jsonify

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
    # 设置数据
    period = range(1990,2015)
    regions = [['110100','浙江','温州']]
    variables = ['国内生产总值','财政收入']
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
    return render_template("provincedataquery.html",period=period,regions=regions,variables=variables)

# 省级数据查询
@myapp.route('/query',methods=['GET', 'POST'])
def query():
    # 设置数据
    period = range(1990,2015)
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
    return render_template("query.html",period=period)

@myapp.route('/ajaxtwo', methods=['POST','GET'])
def ajaxtwo():
    return render_template('ajaxtwo.html')

@myapp.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    #result = a + b
    return jsonify(result=a + b)

@myapp.route('/ajaxtest', methods=['POST','GET'])
def ajaxtest():
    # 设置数据
    period = range(1990,2015)
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
    return render_template('ajaxtest.html',period=period)

@myapp.route('/jquerylearning',methods=['POST','GET'])
def jquerylearning():
    period = range(1990,2015)
    if request.method == 'POST':
        print("hello")
        formdata = request.form
        print(formdata)
        print(formdata.getlist('period'))
        print(formdata.getlist('hregion'))
        print(formdata.getlist('variable'))
    return render_template('jquerylearning.html',period=period)

@myapp.route('/_from_year_get_regions',methods=['POST','GET'])
def from_year_get_regions():
    period_done = request.values.getlist('period_done[]')
    # 这里要调用函数，通过时期获取变量
    region_generated = [24,[{'text':'中国','nodes':[{'text':'北京','nodes':[{'text':'海淀'}]},{'text':'上海'}]}]]
    return jsonify(regions=region_generated)

@myapp.route('/_from_region_get_variables',methods=['POST','GET'])
def from_region_get_variables():
    regions = request.values.getlist('region_selected[]')
    years = request.values.getlist('period_selected[]')
    print(regions)
    print(years)
    # 这里要调用函数，通过时期和区域获得变量
    variable_generated = [
                {
                    "type": "optiongroup",
                    "label": "The Griffins",
                    "children": [
                        { "type": "option", "value": "Peter",  "label": "Peter Griffin"},
                        { "type": "option", "value": "Lois",   "label": "Lois Griffin"},
                        { "type": "option", "value": "Chris",  "label": "Chris Griffin"},
                        { "type": "option", "value": "Meg",    "label": "Meg Griffin"},
                        { "type": "option", "value": "Stewie", "label": "Stewie Griffin"}
                    ]
                },
                {
                    "type": "optiongroup",
                    "label": "Peter's Friends",
                    "children": [
                        { "type": "option", "value": "Cleveland", "label": "Cleveland Brown"},
                        { "type": "option", "value": "Joe",       "label": "Joe Swanson"},
                        { "type": "option", "value": "Quagmire",  "label": "Glenn Quagmire"}
                    ]
                },
                { "type": "option", "value": "Evil Monkey", "label": "Evil Monkey"},
                { "type": "option", "value": "Herbert",     "label": "John Herbert"}
            ]
    return jsonify(variables=variable_generated)