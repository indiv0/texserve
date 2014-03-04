class Config(object):
    SECRET_KEY = 'wKp\x89\xe1\xa3\xf0\xec\x93W\xf4\x8fQ\xf0\xf5\x0f#\xf8\xfe\xc4h+\xcb4'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
