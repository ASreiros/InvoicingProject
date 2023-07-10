from app import app
from werkzeug.security import generate_password_hash, check_password_hash


def validate_password(password, repeat_password):
	error = ""
	capital = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
			   'V', 'W', 'X', 'Y', 'Z']
	number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	hashed_password = generate_password_hash(password)
	if password == "":
		error += "Slaptažodis neįrašytas. "
	elif not password == repeat_password:
		error += "Slaptažodžiai neatitinka. "
	elif len(hashed_password) > 200:
		error += "Slaptažodis per ilgas."
	elif len(password) < 3:
		error += "Slaptažodis per trumpas."
	flag_capital = False
	flag_number = False
	for letter in password:
		if letter in capital:
			flag_capital = True
		elif letter in number:
			flag_number = True
	if flag_number is False or flag_capital is False:
		error += "Slaptažodis neatitinka reikalavimų dėl ženklų. "
	return error


def validate_name(name):
	error = ""
	if name == "":
		error += "Vardas arba pavadinimas neįrašytas. "
	elif len(name) > 100:
		error += "Vardas arba pavadinimas per ilgas. "
	return error


def validate_login(login):
	error = ""
	if login == "":
		error += "Prisijungimo vardas neįrašytas. "
	elif len(login) > 80:
		error += "Prisijungimo vardas per ilgas. "
	return error


def validate_email(email):
	error = ""
	if email == "":
		error += "El. paštas neįrašytas neįrašytas. "
	elif len(email) > 100:
		error += "El. paštas per ilgas. "
	return error

def validate_tax(tax):
# 	I don't assume anything about tax code, different countries has different tax codes.
# 	The only thing I check if it is too long
	error = ""
	if len(tax) > 100:
		error += "Mokesčio kodas per ilgas. "
	return error


def validate_address(address):
	error = ""
	if len(address) > 200:
		error += "Adresas per ilgas. "
	return error


def validate_user_data(user):
	address = user.address
	if not address:
		address = ""
	tax = user.tax_code
	if not tax:
		tax = ""
	vat = user.vat_code
	if not vat:
		vat = ""
	data = {
		'name': user.name,
		'address': address,
		'vat': vat,
		'tax': tax,
		'error': "",
		'p_error': "",
	}
	return data
