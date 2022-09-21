import os

class Config(object):
    SECRET_KEY = 'dev'
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'rabarbar'
