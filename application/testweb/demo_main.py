# coding=UTF-8

import os
from DataWarehouse.database.class_database import Database
from flask import Flask, render_template, request, redirect, url_for, jsonify
from DataWarehouse.data.class_regiondata import RegionData
import json
from bokeh.plotting import figure
from bokeh.embed import components
from werkzeug.utils import secure_filename
import flask.ext.login as flask_login

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

# 创建初始数据
# 导入CEIC数据
db = Database()
con = db.connect('regionDB', 'CEIC')
period = range(1990,2015)
# 创建区域数据
region_list = json.load(open('e:/gitwork/application/testweb/region_ceic.txt'))
variables = con.find().distinct('variable')
rdata = RegionData()
# Our mock database.
users = {'glen.zhang7@gmail.com': {'pw': '123456'}}

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
# add a line renderer with legend and line thickness
p.line(x, y, legend="Temp.", line_width=2)
script, div = components(p)

UPLOAD_FOLDER = 'd:/temp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            project_name = u'创数据'
            company_date = u'华东理工大学商学院 2015'
            return render_template('index.html',project_name=project_name,company_date=company_date)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

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

@app.route("/bokeh")
def bokeh():
    return render_template('bokehtest.html',script=script,div=div)

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
    #result = a + b
    return jsonify(result=a + b)

@app.route('/ajaxtwo', methods=['POST','GET'])
def ajaxtwo():
    return render_template('ajaxtwo.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        return render_template('testweb.html',mname=name)
        #return redirect(url_for('login',mname=name))
    return render_template('testweb.html')


if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)