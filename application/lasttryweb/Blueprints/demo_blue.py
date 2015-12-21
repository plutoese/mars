from flask import Flask, Blueprint

app = Flask(__name__)
hello = Blueprint('hello',__name__)

@hello.route('/')
def hello_world():
    return 'Hello World! I am a bad person!@**@'

app.register_blueprint(hello)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
