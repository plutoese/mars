# coding=UTF-8

class BaseConfig(object):
    "基本配置"
    SECRET_KEY = 'A random secret key'
    DEBUG = True

class ProductionConfig(BaseConfig):
    "生产性配置"
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    "开发性配置"
    DEBUG = True
    SECRET_KEY = 'Another random secret key'
