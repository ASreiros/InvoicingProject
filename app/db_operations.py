from app import app, db
from app import models
from werkzeug.security import generate_password_hash, check_password_hash


def create_demo_user():
	if not models.User.query.filter_by(id=1).first():
		user = models.User(username='demo', name='demo',
						password=generate_password_hash('A123'),
						email='demo@demo.lt',
						)

		try:
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			print(e)
		else:
			data = {
				'name': 'DEMO',
				'vat': 'LT123456789',
				'tax': "123456789",
				'address': "Taikos pr. 1, Klaipėda",
			}
			edit_user(1, data)
			invoice_data = {'type': 'pvm sąskaita-faktūra', 'date': '2023-06-30', 'series': 'INV', 'number': '1', 'seller-name': 'demo', 'seller-tax': '123456789', 'seller-vat-tax': 'LT123456789', 'seller-address': 'Taikos pr. 1, Klaipėda', 'buyer-name': 'Demo pirkėjas', 'buyer-tax': '1238578', 'buyer-vat-tax': '', 'buyer-address': '', 'beforeVat': '440.68', 'vat': '92.54', 'vatTypas': '21', 'afterVat': '533.22', 'id': 'noid', 'lines': [{'product': 'Kedės', 'quantity': '12', 'unit': 'vnt', 'price': '10', 'total': '120'}, {'product': 'Sofa', 'quantity': '1', 'unit': 'vnt', 'price': '155.32', 'total': '155.32'}, {'product': 'Stalas', 'quantity': '3', 'unit': 'vnt', 'price': '55.12', 'total': '165.36'}]}
			save_invoice_to_db(invoice_data, 1)

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


def get_demo_user():
	user = models.User.query.filter_by(username='demo').first()
	return user


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
							 full_number=data["series"] + data['number'],
							 date=data['date'],
							 type=data['type'],
							 vat_setting=data['vatTypas'],
							 buyer_name=data["buyer-name"],
							 buyer_tax=data["buyer-tax"],
							 buyer_vat=data["buyer-vat-tax"],
							 buyer_address=data["buyer-address"],
							 sum_before_vat=data['beforeVat'],
							 vat=data['vat'],
							 sum_after_vat=data['afterVat'],
							 user_id=user_id)

	try:
		db.session.add(invoice)
		db.session.commit()
	except Exception as e:
		print(e)
		return False
	else:

		for line in data['lines']:
			line['invoice_id'] = data['id']
		if save_invoice_lines(data['lines']):
			return [True, invoice.id]
		else:
			delete_invoice(invoice.id, user_id)
			return [False, invoice.id]


def edit_invoice_to_db(data, user_id):
	print("invoice data:", data)
	invoice_info = {
		'series': data["series"],
		'number': data['number'],
		'full_number': data["series"] + data['number'],
		'date': data['date'],
		'type': data['type'],
		'vat_setting': data['vatTypas'],
		'buyer_name': data["buyer-name"],
		'buyer_tax': data["buyer-tax"],
		'buyer_vat': data["buyer-vat-tax"],
		'buyer_address': data["buyer-address"],
		'sum_before_vat': data['beforeVat'],
		'vat': data['vat'],
		'sum_after_vat': data['afterVat']
	}

	invoice = db.session.query(models.Invoice).filter_by(id=data['id'], user_id=user_id).update(invoice_info)
	print("edit invoice ",invoice)
	try:
		db.session.commit()
		print("we are here")
	except Exception as e:
		print(e)
		return False
	else:
		if invoice:
			if not delete_lines(data['id']):
				return False
			for line in data['lines']:
				line['invoice_id'] = data['id']
			if save_invoice_lines(data['lines']):
				return True
			else:
				return False
		else:
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
	invoice = models.Invoice.query.filter_by(id=int(invoice_id), user_id=user_id).first()
	try:
		db.session.delete(invoice)
		db.session.commit()
	except Exception as e:
		print("lines Error: ", e)
		return False
	else:
		return True


def collect_invoices(user_id):
	invoices = models.Invoice.query.filter_by(user_id=user_id).all()
	return invoices


def get_invoice_number(user_id, series):
	invoices = models.Invoice.query.filter_by(user_id=user_id, series=series).all()
	high_number = 0
	for inv in invoices:
		if inv.number > high_number:
			high_number = inv.number
	return high_number + 1


def get_invoice(invoice_id, user_id):
	invoice = models.Invoice.query.filter_by(user_id=user_id, id=invoice_id).first()
	return invoice


def get_lines(invoice_id):
	lines = models.Line.query.filter_by(invoice_id=invoice_id).all()
	return lines


def delete_lines(invoice_id):
	lines = models.Line.query.filter_by(invoice_id=invoice_id).delete()
	try:
		db.session.commit()
	except Exception as e:
		print("lines Error: ", e)
		return False
	else:
		return True
