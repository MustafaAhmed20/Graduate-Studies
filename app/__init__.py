from json import JSONEncoder

from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager


from config import config

db = SQLAlchemy()

# auth
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	# bootstrap.init_app(app)
	# mail.init_app(app)
	# moment.init_app(app)
	
	db.init_app(app)
	login_manager.init_app(app)
	#Session(app)

	# attach routes and custom error pages here
	from .main import main as main_blueprint
	from .auth import auth as auth_blueprint

	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint)
	
	return app

# make possible to use 'to_json' methods inside the classes
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

def validation(field, Type):
	""" vlaidation function .
		type = username the length between(5-28)
		type = password the length between(5-28)
		type = phone the length between(10-14) and is digit
		type = email takes the email shape
		type = digit must be numbers"""

	if not field:
		return False

	elif Type == "username" or 'password':
		if not (5 <= len(field) <= 28):
			return False

	elif Type == "phone":
		if not (10 <= len(field) <= 14) or not (field.isdigit()):
			return False

	elif Type == "digit":
		if not field.isdigit():
			return False
	
	elif Type == "email":
		
		import re
		email ='info@domain.com'
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

		if match == None:
			return False
	
	else :
		# not valid type
		raise KeyError("not valid parameter 'Type' .")

	return True

# response model
def gResponse(Type='noLink', status=True, message='', link='', data=None): 
	""" global response model with two types:
		- with link
		- no link
		..
		parameters :
		. Type
		. status
		. message
		. link
		"""
	if status not in (True, False):
		raise KeyError("not valid parameter 'status' .")
	if not type(message) is str:
		raise KeyError("not valid parameter 'message' .")
	if not type(link) is str:
		raise KeyError("not valid parameter 'link' .")

	if status:
		status = 'success'
	else:
		status = 'error'
	
	
	result = {"status": status}

	if data:
		result['data'] = data

	if message:
		result['message'] = message

	if Type == 'noLink':
		return result
	
	elif Type == 'withLink':
		result['link'] = link
		return result
	
	else:
		raise KeyError("not valid parameter 'Type' .")


