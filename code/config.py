from flask import Flask, render_template, request, redirect, session, url_for, escape ,jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import os
from datetime import datetime
import string
from secrets import choice

from json import JSONEncoder


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123pm@localhost/uni'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

alphabet = string.ascii_letters + string.digits
app.secret_key = ''.join(choice(alphabet) for i in range(24))

Session(app)


def visited_required(f):
	"""
	Decorate routes to require login.

	http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
	"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("visited") is None:
			return redirect('/notAllowed')
			#return f(*args, **kwargs)
		return f(*args, **kwargs)
	return decorated_function

def login_required(*permissionType):
	
	def decorator(f):
		"""
		Decorate routes to require login.

		http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
		"""
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if session.get("logedIn") is None:
				return redirect('/notAllowed')
			else:
				# the permission of the user that logedIn
				if permissionType:
					# get sure all parameters are strings
					if not all(map(lambda x:True if type(x) is str else False, permissionType)):
						return redirect('/error')
					
					permission = session.get("user_permission")
					if permission not in permissionType:
						return redirect('/notAllowed')
			# valid login
			return f(*args, **kwargs)
		return decorated_function
	
	return decorator

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    #CELERY_RESULT_BACKEND='redis://localhost:6379'
    result_backend='redis://localhost:6379'
)

# make possible to use 'to_json' methods inside the classes
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default
