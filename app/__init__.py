from flask import Flask
from flask_sqlalchemy import SQLAlchemy, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)

app.config['SECRET_KEY'] = "horse-battery"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///invoice.db"
db = SQLAlchemy(app)



from app import views
from app import calculate
from app import db_operations
from app import models


with app.app_context():
    db.create_all()







from app import views
from app import calculate
from app import db_operations