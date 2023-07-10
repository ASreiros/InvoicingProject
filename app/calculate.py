from app import app

def calculate_invoice_lines(req):
	total_before_VAT = 0
	for line in req['lines']:
		line['total'] = round(float(line['price'])* float(line['vnt']), 2)
		total_before_VAT += line['total']
	req['total_before_VAT'] = round(total_before_VAT, 2)
	if req['inv-type'] == "pvm sąskaita-faktūra" or req['inv-type'] == "invoice":
		vat_types = {
			'21': 0.21,
			'9': 0.09,
			'5': 0.05,
			'6': 0.06,
			'0': 0,
			'21a': 0.21,
		}

		koeficent = vat_types[req['vat-type']]
		req['VAT'] = round(req['total_before_VAT'] * koeficent, 2)
		if not req['vat-type'] == '21a':
			req['total_after_VAT'] = round(req['total_before_VAT'] + req['VAT'], 2)
		else:
			req['total_after_VAT'] = round(req['total_before_VAT'])
	else:
		req['VAT'] = 0
		req['total_after_VAT'] = 0
	return req
