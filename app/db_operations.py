from app import app, db
from app import models
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(data):
	user = models.User(username=data['r_login'], name=data['r_name'], password=data['r_password'], email=data['r_email'])
	try:
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		print(e)
		return False
	else:
		return user


def check_user(data):
	user = models.User.query.filter_by(username=data['s_login']).first()
	check_password_hash(user.password, data['s_password'])
	print(user)
	print()
	if user and check_password_hash(user.password, data['s_password']):
		return user
	else:
		return False







