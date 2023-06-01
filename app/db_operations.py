from app import app
import sqlite3


def connect_db():
	db = sqlite3.connect("projectInvoice.db")
	cursor = db.cursor()
	return cursor


def add_user(data):
	db = sqlite3.connect("projectInvoice.db")
	cursor = db.cursor()
	print(data)
	try:
		cursor.execute(f"""
		INSERT INTO users (login, name, email, password)
		VALUES 
			('{data['r_login']}', '{data['r_name']}', '{data['r_email']}', '{data['r_password']}');
		""")
		result = cursor.fetchall()
		print(result)
		db.commit()
		db.close()
	except Exception as e:
		print(e)
		return e
	else:
		print("user added")
		return 1







