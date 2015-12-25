# coding=UTF-8

from flask import Blueprint

myapp = Blueprint('myapp', __name__)

@myapp.route('/')
def index():
    return "Hello World!@@"