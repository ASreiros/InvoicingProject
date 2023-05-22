
def calculate_invoice_lines(req):
	print("req:", req)
	total_before_VAT = 0
	for line in req['lines']:
		line['total'] = round(float(line['price'])* float(line['vnt']), 2)
		total_before_VAT += line['total']
		print("line", line)
	req['total_before_VAT'] = total_before_VAT
	if req['inv-type'] == "pvm sąskaita-faktūra" or req['inv-type'] == "invoice":
		vat_types = {
			'21': 0.21,
			'9': 0.09,
			'5': 0.05,
			'6': 0.06,
			'0': 0,
		}

		koeficent = vat_types[req['vat-type']]
		req['VAT'] = round(req['total_before_VAT'] * koeficent, 2)
		print(koeficent, req['total_before_VAT'])

		if not req['vat-type'] == '21a':
			req['total_after_VAT'] = round(req['total_before_VAT'] + req['VAT'], 2)
	else:
		print(req['inv-type'])
		req['VAT'] = 0
		req['total_after_VAT'] = 0
	return req
