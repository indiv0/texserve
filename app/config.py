import os

GIT_NOTES_REPO_URL = 'https://github.com/Indiv0/notes.git'

PRODUCTION = True

if PRODUCTION:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
else:
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    BUCKET_NAME = ''


class Config(object):
    SECRET_KEY = 'wKp\x89\xe1\xa3\xf0\xec\x93W\xf4\x8fQ\xf0\xf5\x0f#\xf8\xfe\xc4h+\xcb4'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
