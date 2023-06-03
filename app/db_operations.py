from app import app, db
from app import models
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(data):
	user = models.User(username=data['r_login'], name=data['r_name'], password=generate_password_hash(data['r_password']), email=data['r_email'])
	try:
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		print(e)
		return [False, e]
	else:
		return [True, user]


def check_user(data):
	user = models.User.query.filter_by(username=data['s_login']).first()
	if not user:
		return False
	check_password_hash(user.password, data['s_password'])
	print(user)
	if user and check_password_hash(user.password, data['s_password']):
		return user
	else:
		return False


def edit_user(user_id, data):
	user = models.User.query.get(user_id)
	user.name = data['name']
	user.vat_code = data['vat']
	user.tax_code = data['tax']
	user.address = data['address']
	try:
		db.session.add(user)
		db.session.commit()
	except Exception as e:
		print(e)
		return False
	else:
		return True

def update_password(user_id, password):
	user = models.User.query.get(user_id)
	if check_password_hash(user.password, password):
		user.password = generate_password_hash(password)
		try:
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			print(e)
			return False
		else:
			return True
	else:
		return False



def save_invoice_to_db(data, user_id):
	invoice = models.Invoice(series=data["series"],
							 number=data['number'],
							 full_number=data["series"]+data['number'],
							 date=data['date'],
							 type=data['type'],
							 vat_setting=data['vatTypas'],
							 buyer_name=data["buyer-name"],
							 buyer_tax =data["buyer-tax"],
							 buyer_vat =data["buyer-vat-tax"],
							 buyer_address =data["buyer-address"],
							 sum_before_vat =data['beforeVat'],
							 vat =data['vat'],
							 sum_after_vat =data['afterVat'],
							 user_id=user_id)
	try:
		db.session.add(invoice)
		db.session.commit()
	except Exception as e:
		print(e)
		return False
	else:
		for line in data['lines']:
			line['invoice_id'] = invoice.id
		if save_invoice_lines(data['lines']):
			return True
		else:
			delete_invoice(invoice.id, user_id)
			return False


def save_invoice_lines(line_data):
	lines_to_add = [models.Line(**row) for row in line_data]
	try:
		db.session.add_all(lines_to_add)
		db.session.commit()
	except Exception as e:
		print("lines Error: ", e)
		return False
	else:
		return True


def delete_invoice(invoice_id, user_id):
	invoice = models.Invoice.query.filter_by(id=invoice_id, user_id=user_id).first()
	try:
		db.session.delete(invoice)
		db.session.commit()
	except Exception as e:
		print("lines Error: ", e)
		return False
	else:
		return True
