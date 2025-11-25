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

# https://gist.github.com/asyd/a7aadcf07a66035ac15d284aef10d458
# Ensure FOREIGN KEY for sqlite3
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect to login page if not authenticated
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

from flaskapp import main, models
