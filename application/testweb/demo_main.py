# coding=UTF-8

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    project_name = u'创数据'
    company_date = u'华东理工大学商学院 2015'
    return render_template('index.html',project_name=project_name,company_date=company_date)

@app.route("/query",methods=['POST', 'GET'])
def query():
    return render_template('query.html')

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