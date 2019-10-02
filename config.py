class Config:
    SECRET_KEY = 'SAHFDKSDJFL;JA;KJF'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STFU_MAIL_SUBJECT_PREFIX = '[STFU]'
    MAIL_SENDER = 'STFU Admin<development_team@qq.com>'
    MAIL_ADMIN = 'development_team@qq.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'development_team@qq.com'
    MAIL_PASSWORD = 'pofxzfsrkytzegcb'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:154202@localhost/ceshi'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:154202@localhost/ceshi'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:154202@localhost/ceshi'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
