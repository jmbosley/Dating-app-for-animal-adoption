import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # we can set these in the environment later
    SECRET_KEY = "placeholderkey" # needed for forms/site security which we haven't done yet
    # specify use of sqllite
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "flaskapp.db")