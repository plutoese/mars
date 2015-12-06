# coding=UTF-8

from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'

class NameForm(Form):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')

@app.route("/")
def index():
    title = u'世界上的另一个'
    return render_template('index.html',title=title)

@app.route("/hello")
def hello():
    return render_template('hello.html')

@app.route("/regionquickquery",methods=['GET','POST'])
def quick_query():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        print(name)
    return render_template('regionquickquery.html',form=form)

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)