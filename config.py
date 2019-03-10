import os
from secrets import choice
import string
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))

alphabet = string.ascii_letters + string.digits

class Config:
	SECRET_KEY = ''.join(choice(alphabet) for i in range(24))

	# Configure session to use filesystem (instead of signed cookies)
	SESSION_FILE_DIR = mkdtemp()
	SESSION_PERMANENT = False
	SESSION_TYPE = "filesystem"

	CELERY_BROKER_URL = 'redis://localhost:6379'
	result_backend = 'redis://localhost:6379'
	

	#SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	#FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	#FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	#FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	# MAIL_SERVER = 'smtp.googlemail.com'
	# MAIL_PORT = 587
	# MAIL_USE_TLS = True
	# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql://root:123pm@localhost/uni'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:123pm@localhost/testing'

class ProductionConfig(Config):
	#SQLALCHEMY_DATABASE_URI = 'mysql://root:123pm@localhost/uni'
	pass
	

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}