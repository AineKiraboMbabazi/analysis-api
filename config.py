import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'this is my secret key'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True

app_config={
    'development':DevelopmentConfig,
    'testing': TestingConfig
    
}
