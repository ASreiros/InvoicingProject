from flask import Flask

app = Flask(__name__)



from app import views
from app import calculate
from app import db_creation
from app import db_operations