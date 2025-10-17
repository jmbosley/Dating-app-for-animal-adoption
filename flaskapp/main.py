# routes
from flask import Flask, render_template, request, redirect
from flaskapp import app # importing the flask app from our package defined in __init__.py
from flaskapp import db
from flaskapp.models import publicAccount
import sqlalchemy as sa

# old datastore code:
# from google.cloud import datastore
# from google.cloud.datastore.query import And, PropertyFilter
# datastore_client = datastore.Client()

ACCOUNTS = "accounts"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'phoneNumber', 'password']

example_SQL_account = publicAccount(firstName='Billy', lastName='Smith', email="fake@gmail.com", phoneNumber="123", password="password")

# Error Message
#ERROR_MISSING_VALUE = "Not all required values were provided"

@app.route("/")
def root():
    return render_template("index.html", title="Datastore and Firebase Auth Example")

# sqllite demonstration using model
@app.route('/sqldemo', methods=['GET', 'POST'])
def sql_demo():
    if request.method == 'GET': # display page
        query = sa.select(publicAccount).where(publicAccount.phoneNumber != "5") # random query
        # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html execute or scalars will work
        accounts = db.session.scalars(query)
        return render_template("sqlexample.html", title="SQL example", results = accounts)

    if request.method == 'POST': # add account
        content = request.get_json()
        new_account = publicAccount(firstName=content['firstName'], lastName=content['lastName'], email=content['email'], 
                                    phoneNumber=content['phoneNumber'], password=content['password'])
        db.session.add(new_account) # INSERT
        db.session.commit()
        return redirect("/sqldemo")


# Create a Public Account
@app.route('/' + ACCOUNTS, methods=['POST'])
def post_businesses():
    # get account info
    content = request.get_json()

    # check if minimum info was provided
    if not (set(MIN_ACCOUNT).issubset(content)):
        return ERROR_MISSING_VALUE, 400
    
    # Create new Account
    new_account = datastore.Entity(key=datastore_client.key(ACCOUNTS))
    new_account.update({
        'firstName': content['firstName'],
        'lastName': content['lastName'],
        'email': content['email'],
        'phoneNumber': content['phoneNumber'],
        'password': content['password']
    })
    datastore_client.put(new_account)
    new_account['id'] = new_account.id
    return ("Account was successfully created!", 201)
