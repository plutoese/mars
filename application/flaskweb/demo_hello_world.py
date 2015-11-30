# coding=UTF-8

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    title = u'世界上的另一个'
    return render_template('index.html',title=title)

@app.route("/hello")
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run()