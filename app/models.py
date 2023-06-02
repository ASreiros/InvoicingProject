from app import app, db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200), unique=False)
    vat_code = db.Column(db.String(20), unique=False)
    tax_code = db.Column(db.String(30), unique=False)
    address = db.Column(db.String(200), unique=False)

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
