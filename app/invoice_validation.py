from app import app, db
from app import models
from app import validation


def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False


def unique_invoice_name_check(data, user_id):
	error = ""
	try:
		full_number = data['series'] + data['number']
		repeating_number = models.Invoice.query.filter_by(full_number=full_number, user_id=user_id).first()
		if repeating_number:
			error += "Sąskaitos faktūros numeris neunikalus \n"
		return error
	except Exception as e:
		return "Patikrinti įrašo unikalumą neišėjo. \n"


def invoice_validation(data):
	# I need one more validation if data has all the keys
	vat_settings = ['21', '9', '5', '6', '0', '21a']
	doc_type = ["pvm sąskaita-faktūra", "sąskaita-faktūra", "invoice"]
	error = ""
	print(data)
	try:
		if data["series"] == "" or data['number'] == "":
			error += "Neįrašytas sąskaitos numeris arba serija"
		if len(data['date']) != 10:
			error += "Sąskaitos data klaidinga \n"
		if data["buyer-name"] == "":
			error += "Nenurodytas pirkejo pavadinimas \n"
		if len(data["buyer-name"]) > 80 or len(data["buyer-tax"]) > 80 or len(data["buyer-vat-tax"]) > 80 or len(data["buyer-address"]) > 200:
			error += "Pirkėjo duomenys yra per ilgi \n"
		if data['seller-name'] == "":
			error += "Pardavėjo pavadinimas neįrašytas \n"
		if len(data["seller-name"]) > 80 or len(data["seller-tax"]) > 80 or len(data["seller-vat-tax"]) > 80 or len(data["seller-address"]) > 200:
			error += "Pardavėjo duomenys yra per ilgi \n"
		if not data['type'] in doc_type:
			error += "Klaidingas dokumento tipas \n"
		if not data['vatTypas'] in vat_settings:
			error += "Klaidingas pvm nustatymas"
		if not is_float(data['beforeVat']):
			error += "Suma be PVM turi klaidą \n"
		if not is_float(data['vat']):
			error += "PVM suma turi klaidą \n"
		if not is_float(data['afterVat']):
			error += "Suma su PVM turi klaidą \n"
		for l in range(len(data['lines'])):
			if data['lines'][l]['product'] == "" or data['lines'][l]['unit'] == "" or not is_float(data['lines'][l]['quantity']) or not is_float(data['lines'][l]['price']) or not is_float(data['lines'][l]['total']):
				error += f'Papildykite duomenys eilutejė {l+1} arba ištrinkitė ją. \n'
	except Exception as e:
		print(e)
		return "Dokumentas neturi reikalingu duomenų \n"
	else:
		return error





