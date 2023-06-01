from app import app
import sqlite3


db = sqlite3.connect("projectInvoice.db")

cursor = db.cursor()
try:
	cursor.execute("""CREATE TABLE users (
		id INTEGER PRIMARY KEY,
		login varchar(250) NOT NULL UNIQUE,
		name varchar(250) NOT NULL,
		email varchar(250) NOT NULL UNIQUE,
		password varchar(250) NOT NULL,
		tax_code varchar(30),
		VAT_tax_code varchar(30),
		address varchar(250)
	);""")
except Exception as e:
	print(e)
else:
	print("table created")