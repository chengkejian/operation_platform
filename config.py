#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: ckj 
@file: config.py
@time: 2016/8/16 15:47
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	basdir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'mysql://root:centos@10.10.10.103/yunwei'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = 'mobim'
	MAIL_SERVER = 'smtp.mobimtech.com'
	MAIL_PORT = 25
	# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_USERNAME = 'kejian.cheng@mobimtech.com'
	MAIL_PASSWORD = 'ckj.351373653'
	MOBIM_MAIL_SUBJECT_PREFIX = '[Mobim]'
	MOBIM_MAIL_SENDER = 'kejian.cheng@mobimtech.com'
	MOBIM_ADMIN = '351373653@qq.com'
	FLASKY_POSTS_PER_PAGE = 8
	UPLOAD_FOLDER = 'E:/Android'
	ALLOWED_EXTENSIONS={'png','jpg'}
	PROJECT_ROOT = 'E:/Android/native_R'
	PACKAGE_ROOT = 'E:/Android/package'
	IMIFUN_PACKAGE_SFTP_IP = '119.29.236.26'
	IMIFUN_PACKAGE_SFTP_PORT = 22
	IMIFUN_PACKAGE_SFTP_USER = 'mobim'
	IMIFUN_PACKAGE_SFTP_PASSWD = 'I8rBzeqWsuTzfV4b'
	IMIFUN_PACKAGE_SFTP_PATH = '/data/imi/webapps/static.imifun.com/tmp'
	YUNFAN_PACKAGE_FTP_IP = '183.60.41.18'
	YUNFAN_PACKAGE_FTP_PORT = 6554
	YUNFAN_PACKAGE_FTP_USER = 'imifun'
	YUNFAN_PACKAGE_FTP_PASSWD = '3674ceb5ca763c9420f5d8b203c1f1ad'
	YUNFAN_PACKAGE_SFTP_PATH = '/test/'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

	SQLALCHEMY_DATABASE_URI = 'mysql://root:centos@10.10.10.103/yunwei'

class TestingConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
							  'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
	UPLOAD_FOLDER = '/data/android/code'
	PROJECT_ROOT = '/data/android/code/native_R'
	PACKAGE_ROOT = '/data/android/package'
	IMIFUN_PACKAGE_SFTP_PATH = '/data/imi/webapps/static.imifun.com'
	YUNFAN_PACKAGE_SFTP_PATH = '/'
	SQLALCHEMY_DATABASE_URI = 'mysql://yunwei:mobim.test@10.10.10.125/yunwei'
	@classmethod
	def init_app(cls,app):
		Config.init_app(app)

		import logging
		import logging.config
		logging.config.fileConfig("logging.config")
		# from logging.handlers import RotatingFileHandler
		# file_handler = RotatingFileHandler('tmp/test.log', 'a', 1 * 1024 * 1024, 10)
		# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		# app.logger.setLevel(logging.INFO)
		# file_handler.setLevel(logging.INFO)
		# app.logger.addHandler(file_handler)

config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,
	'default':DevelopmentConfig
}