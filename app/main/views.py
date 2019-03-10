from flask import render_template, session, redirect, url_for

from . import main
from .. import db
from ..models import *

@main.route('/')
def index():
	return 'hello world'