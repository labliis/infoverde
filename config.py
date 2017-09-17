class Config(object):
    SECRET_KEY = '1234'
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jhon:andrea@localhost/CO2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False