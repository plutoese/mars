# coding=UTF-8

from flask import Flask
from webapp.dist.views import myapp

app = Flask(__name__)
app.config.from_object('webapp.config.DevelopmentConfig')

app.register_blueprint(myapp)

