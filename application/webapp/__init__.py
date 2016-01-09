# coding=UTF-8

from flask import Flask
from webapp.dist.views import myapp
from webapp.dist.models import UPLOAD_FOLDER


app = Flask(__name__)
app.config.from_object('webapp.config.DevelopmentConfig')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

app.register_blueprint(myapp)

