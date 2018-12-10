# -*- encoding: utf-8 -*-
# Copyright 2018 Vinzor Co.,Ltd.
#
# comment
#
# 18-10-13 leo : Init

import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_REDIRECT = False
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
    # Sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_POOL_RECYCLE = os.environ.get('SQLALCHEMY_POOL_RECYCLE') or 3600
    # Jwt_extended
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_CHECKED = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    # Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://:' + os.environ.get(
        'REDIS_PASSWORD') + '@localhost:6379/0'
    # restful
    PROPAGATE_EXCEPTIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://' + os.environ.get('DATABASE_USER') + ':' + \
        os.environ.get('DATABASE_PASSWORD') + \
        '@127.0.0.1:3306/subsidy_dev?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://' + os.environ.get('DATABASE_USER') + ':' + \
        os.environ.get('DATABASE_PASSWORD') + \
        '@127.0.0.1:3306/subsidy_test?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://' + os.environ.get('DATABASE_USER') + ':' + \
        os.environ.get('DATABASE_PASSWORD') + \
        '@127.0.0.1:3306/subsidy?charset=utf8'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}