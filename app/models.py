from app import app, db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200), unique=False)
    vat_code = db.Column(db.String(20), unique=False)
    tax_code = db.Column(db.String(30), unique=False)
    address = db.Column(db.String(200), unique=False)
    series = db.Column(db.String(20), unique=False)
    invoices = db.relationship(
        'Invoice',
        back_populates='user',
        # delete customer orders when customer deleted
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = password
        self.series = "INV"

    def __repr__(self):
        return '<User %r>' % self.username



class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(30), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    full_number = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(30), unique=False, nullable=False)
    type = db.Column(db.String(30), unique=False, nullable=False)
    vat_setting = db.Column(db.String(30), unique=False, nullable=False)
    buyer_name = db.Column(db.String(80), unique=False, nullable=False)
    buyer_tax = db.Column(db.String(80), unique=False, nullable=True)
    buyer_vat = db.Column(db.String(80), unique=False, nullable=True)
    buyer_address = db.Column(db.String(200), unique=False, nullable=True)
    sum_before_vat = db.Column(db.Float, unique=False, nullable=False)
    vat = db.Column(db.Float, unique=False, nullable=False)
    sum_after_vat = db.Column(db.Float, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship(
        'User',
        back_populates='invoices',
    )
    lines = db.relationship(
        'Line',
        back_populates='invoice',
        # delete customer orders when customer deleted
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), unique=False)
    quantity = db.Column(db.Float, unique=False)
    unit = db.Column(db.String(10), unique=False)
    price = db.Column(db.Float, unique=False)
    total = db.Column(db.Float, unique=False)

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id', ondelete='CASCADE'), nullable=False, index=True)
    invoice = db.relationship(
        'Invoice',
        back_populates='lines',
    )


