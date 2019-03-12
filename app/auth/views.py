from flask import render_template, request, escape, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from . import auth
from .. import validation, gResponse, db
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	
	# check if the fields submited
	try:
		email = escape(request.form['email'])
		password = escape(request.form['password'])
	except Exception as e:
		message = 'missing fields'
		result = gResponse(status=False, message=message)
		
		return jsonify(result), 400

	# validate the fileds
	if not validation(email, Type="email") or not validation(password, Type='password'):
		message = "fileds did't pass the validaion"
		result = gResponse(status=False, message=message)
		return jsonify(result), 403

	# check if the user exist .
	user = User.query.filter_by(email=email).first()

	# loged-In the user
	if user is not None and user.checkPassword(password):
		# logout first
		logout_user()
		
		# login
		login_user(user)
		link = f'/main?user={user.id}'

		# success
		return jsonify(gResponse(Type='withLink', link=link))

	else:
		# Wrong email or password
		message = 'username or password is wrong'
		return jsonify(gResponse(status=False, message=message)), 403

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
	logout_user()
	
	link = '/'
	
	# success
	return jsonify(gResponse(Type='withLink', link=link))

@auth.route('/registration', methods=['GET', 'POST'])
def registration():
	
	if request.method == 'GET':
		#return render_template('registration.html')
		return render_template('r.html')

	# check if the fields submited
	try:
		email = escape(request.form['email'])
		password = escape(request.form['password'])
		rePassword = escape(request.form['re-password'])
		name = escape(request.form['name'])
		permission = escape(request.form['permission'])
	except Exception as e:
		message = 'missing fields'
		result = gResponse(status=False, message=message)
		
		return jsonify(result), 400

	# validate the fileds
	if not validation(email, Type="email") or not validation(password, Type='password')\
		or not validation(name, Type='username') or not validation(name, Type='digit') or\
		password != rePassword:
		
		message = "fileds did't pass the validaion"
		result = gResponse(status=False, message=message)
		return jsonify(result), 403

	# check if the user exist before.
	user = User.query.filter_by(email=email).first()
	if user:
		message = 'user exist before'
		result = gResponse(status=False, message=message)
		return jsonify(result), 400

	# new user
	user = User(email=email, password=generate_password_hash(password),\
	 name=name, permission=permission, status=0)

	db.session.add(user)
	db.session.commit()

	# success
	message = 'you are successfully registered'
	return jsonify(gResponse(message=message))
