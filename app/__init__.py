from flask import Flask
from flask_sqlalchemy import SQLAlchemy, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = "horse-battery"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///invoices_data.db"
db = SQLAlchemy(app)


from app import views
from app import calculate
from app import db_operations
from app import models
from app import validation
from app import invoice_validation

with app.app_context():
    db.create_all()
    db_operations.create_demo_user()


login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))




from app import views
from app import calculate
from app import db_operations
