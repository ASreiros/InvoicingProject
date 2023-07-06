from app import app
import os
from time import time
from fpdf import FPDF
from app import db_operations

def create_pdf(user, invoice_id):

	delete_old_pdf()
	pdf = FPDF()
	pdf.add_page()
	print(user.name)
	invoice = db_operations.get_invoice(invoice_id=invoice_id, user_id=user.id)
	pdf.set_margins(10, 10, 10)
	pdf.add_font(fname='app/static/font/DejaVuSans-Bold.ttf', style='B', family='dejavu', uni=True)
	pdf.add_font(fname='app/static/font/DejaVuSansCondensed.ttf', family='dejavu', uni=True)
	pdf.set_font('dejavu', size=14)
	if invoice:
		lines_info = db_operations.get_lines(invoice_id)
		l_txt = ""
		if lines_info:
			for line in lines_info:
				print(line)
				l_txt +=f"""
					<tr>
					  	<td align="left">{line.product}</td>
					  	<td align="center" >{line.quantity}</td>
						<td align="center" >{line.unit}</td>
					  	<td align="center" >{line.price}</td>
					  	<td align="right" >{line.total}</td>
					</tr>
				"""

		lines_text = f"""
			<table width="100%" align="center">
				<thead>
				</thead>
			  	<tbody>
			  		<tr>
					  	<td align="left" width="40%"><b>Prekių pavadinimas</b></td>
					  	<td align="center" width="15%"><b>Kiekis</b></td>
						<td align="center" width="15%"><b>Mat. vnt.</b></td>
					  	<td align="center" width="15%"><b>Kaina</b></td>
					  	<td align="right" width="15%"><b>Suma</b></td>
					</tr>
					{l_txt}
			  	</tbody>
			</table>
		"""
		doc_type = invoice.type
		if doc_type == "sąskaita-faktūra":
			ending_txt = f"""
							<tr>
							  <td align="left" width="40%"></td>
							  <td align="left" width="30%">Suma:</td>
							  <td align="right" width="30%">{invoice.sum_before_vat}</td>
							</tr>
			"""
		else:
			setting = f'{invoice.vat_setting}%'
			print(setting)
			if setting == "21a%":
				setting = "21% Atvirkštinis apmokestinimas"
			ending_txt = f"""
							<tr>
							  <td align="left" width="40%"></td>
							  <td align="left" width="30%">Suma be PVM:</td>
							  <td align="right" width="30%">{invoice.sum_before_vat}</td>
							</tr>
							<tr>
							  <td align="left"></td>
							  <td align="left">PVM {setting}:</td>
							  <td align="right" >{invoice.vat}</td>
							</tr>
							<tr>
							  <td align="left"></td>
							  <td align="left">Suma su PVM:</td>
							  <td align="right">{invoice.sum_after_vat}</td>
							</tr>
			"""


		ending = f"""
					<table width="100%" align="center">
						<thead>
						</thead>
					  	<tbody>
							{ending_txt}
						</tbody>
					</table>
					"""



		pdf.write_html(f"""
		  <h2 align="center">{doc_type.upper()}</h2>
		  <p align="center">{invoice.full_number}</p>
		  <p align="center">{invoice.date}</p>
		  <table width="100%" align="center">
			  <thead>
			  </thead>
			  <tbody>
				<tr>
				  <td align="left" width="40%"><b>Pardavėjas:</b></td>
				  <td width="20%"></td>
				  <td align="left" width="40%"><b>Pirkėjas:</b></td>
				</tr>
				<tr>
				  <td align="left" >{user.name}</td>
				  <td></td>
				  <td align="left" >{invoice.buyer_name}</td>
				</tr>
				<tr>
				  <td align="left" ><b>Reg. kodas:</b></td>
				  <td></td>
				  <td align="left" ><b>Reg. kodas:</b></td>
				</tr>
				<tr>
				  <td align="left" >{user.tax_code}</td>
				  <td></td>
				  <td align="left" >{invoice.buyer_tax}</td>
				</tr>
				<tr>
				  <td align="left" ><b>PVM kodas:</b></td>
				  <td ></td>
				  <td align="left" ><b>PVM kodas:</b></td>
				</tr>
				<tr>
				  <td align="left" >{user.vat_code}</td>
				  <td ></td>
				  <td align="left" >{invoice.buyer_vat}</td>
				</tr>
				<tr>
				  <td align="left" ><b>Adresas:</b></td>
				  <td ></td>
				  <td align="left" ><b>Adresas:</b></td>
				</tr>
				<tr>
				  <td align="left" >{user.address}</td>
				  <td ></td>
				  <td align="left" >{invoice.buyer_address}</td>
				</tr>
			  </tbody>
			</table>
			{lines_text}
			{ending}
		  """)
		name = f'{user.name}-{invoice.full_number}.pdf'
	else:
		pdf.write_html(f"""
		  <h2 align="center">Dokumentas nepriklauso šitam vartuotojui</h2>
		  """)
		name = "blank.pdf"
	pdf.output(f"app/invoice/{name}")
	return name



def delete_old_pdf():
	cwd = os.getcwd()
	files = os.listdir(f'{cwd}/app/invoice')
	now = time()
	for file in files:
		full_path = f'{cwd}/app/invoice/{file}'
		c_time = os.path.getmtime(full_path)
		if now - 15 > c_time:
			try:
				os.remove(full_path)
			except Exception as e:
				print(e)
			else:
				pass

