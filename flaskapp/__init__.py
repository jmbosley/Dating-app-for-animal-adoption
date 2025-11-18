# create package with __init__: tells datingapp.py how to run the app
from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app) # checks config and makes db from uri
migrate = Migrate(app, db) # can update database layout based on models.py

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect to login page if not authenticated
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

from flaskapp import main, models
