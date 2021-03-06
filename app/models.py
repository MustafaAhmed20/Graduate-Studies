from . import db, login_manager
import datetime
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import check_password_hash

# user loader .. used py Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), nullable=False, unique=True)
	password = db.Column(db.TEXT, nullable=False)
	name = db.Column(db.String(80), nullable=False)
	
	permission = db.Column(db.Integer, db.ForeignKey('permission.id'))

	# 0 - active / 1 - wait for acceptance or confirm / 2 - Blocked / 3 - deleted
	status = db.Column(db.Integer, nullable=False, default=0)

	def to_json(self):
		p = Permission.query.get(self.permission).name
		return {'name':self.name, 'email': self.email, 'permission':p}
	
	def checkPassword(self, password):
		return check_password_hash(self.password, password)

class Request(db.Model):
	__tablename__ = 'request'
	id = db.Column(db.Integer, primary_key=True)
	requestID = db.Column(db.TEXT)
	date = db.Column(db.DATE, nullable=False, default=datetime.datetime.utcnow)
	
	# 0 -  / 1 -  / 2 -  / 3 - 
	status = db.Column(db.Integer, nullable=False, default=0)

	division = db.Column(db.Integer, db.ForeignKey('division.id'))
	
	form1 = db.Column(db.Integer, db.ForeignKey('form1.id'))
	form2 = db.Column(db.Integer, db.ForeignKey('form2.id'))
	form3 = db.Column(db.Integer, db.ForeignKey('form3.id'))
	form4 = db.Column(db.Integer, db.ForeignKey('form4.id'))

	def to_json(self):
		form1 = Form1.get(self.form1)
		form2 = Form2.get(self.form2)
		form3 = Form3.get(self.form3)
		form4 = Form4.get(self.form4)
		division = Division.get(self.division)

		return {'requestID':self.requestID,
				'date':self.date,
				'division':division.to_json(),
				'status':self.status,
				'form1':form1.to_json(),
				'form2':form2.to_json(),
				'form3':form3.to_json(),
				'form4':form4.to_json()}
	
class Division(db.Model):
	__tablename__ = 'division'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	def to_json(self):
		return self.name

class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), nullable=False, unique=True)
	message = db.Column(db.TEXT, nullable=False)

	# 0 - seen / 1 - not seen
	seen = db.Column(db.Integer, nullable=False)

	def to_json(self):
		return{'email':self.email,
				'message':self.message}

class Form1(db.Model): 
	__tablename__ = 'form1'
	id = db.Column(db.Integer, primary_key=True)
	nameAR = db.Column(db.TEXT, nullable=False)
	nameEN = db.Column(db.TEXT, nullable=False)
	nationalNumber = db.Column(db.TEXT)
	nationality = db.Column(db.TEXT)
	birthDate = db.Column(db.DATE, nullable=False)

	# multi-phone will sprate with ';'
	phone = db.Column(db.TEXT, nullable=False)
	email = db.Column(db.TEXT, nullable=False)
	job = db.Column(db.TEXT)

	def to_json(self):
		if ';' in phone:
			phone = phone.split(';')
		else:
			phone = self.phone
		return{'nameAR':self.nameAR,
				'nameEN':self.nameEN,
				'nationalNumber':self.nationalNumber,
				'nationality':self.nationality,
				'birthDate':self.birthDate,
				'phone':phone,
				'email':self.email,
				'job':self.job}

class Form2(db.Model):
	__tablename__ = 'form2'
	id = db.Column(db.Integer, primary_key=True)
	degree =  db.Column(db.Integer, db.ForeignKey('degree.id'))
	date = db.Column(db.DATE , nullable=False)
	university = db.Column(db.TEXT, nullable=False)
	division =  db.Column(db.Integer, db.ForeignKey('division.id'))

	def to_json(self):
		degree = Degree.get(self.degree)
		division = Division.get(self.division)

		return{'degree':degree.to_json(),
				'date':self.date,
				'university':self.university,
				'division':division.to_json()}

class Form3(db.Model):
	__tablename__ = 'form3'
	id = db.Column(db.Integer, primary_key=True)
	degree =  db.Column(db.Integer, db.ForeignKey('degree.id'))
	division =  db.Column(db.Integer, db.ForeignKey('division.id'))
	message = db.Column(db.TEXT)

	def to_json(self):
		degree = Degree.get(self.degree)
		division = Division.get(self.division)

		return{'degree':degree.to_json(),
				'division':division.to_json(),
				'message':self.message}

class Form4(db.Model):
	__tablename__ = 'form4'
	id = db.Column(db.Integer, primary_key=True)

	# name of the files sprated by ';'
	attached = db.Column(db.TEXT)

	# 0 - self / 1 - other
	sponsor = db.Column(db.Integer, nullable=False)

	def to_json(self):
		return 'self' if self.sponsor == 0 else 'other'

class Degree(db.Model):
	__tablename__ = 'degree'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	def to_json(self):
		return self.name

class Permission(db.Model):
	__tablename__ = 'permission'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False, unique=True, index=True)
	users = db.relationship("User")

	def to_json(self):
		return {'id':self.id, 'name':self.name}
		
'''
if __name__ == "__main__":
	
	while True:		
		sure = input(
			"""are you sure you want to drop all the tables before create the tables again ?.\nyou will lose all data (y/n):  """)
		if not (sure=='y' or sure=='n'):
			print("please Enter 'y' or 'n' .")
			continue
		if sure == 'y':
			# drop all the tables
			db.drop_all()
			
			# create all tables
			db.create_all()

			admin = Permission(name='admin')
			db.session.add(admin)
			db.session.commit()

		else:
			break

		break

'''