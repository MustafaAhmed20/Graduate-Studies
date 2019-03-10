from json import JSONEncoder

from flask import Flask, render_template, request, redirect, session, url_for, escape ,jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


from config import config

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	# bootstrap.init_app(app)
	# mail.init_app(app)
	# moment.init_app(app)
	db.init_app(app)
	Session(app)

	# attach routes and custom error pages here
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	return app

# make possible to use 'to_json' methods inside the classes
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default