# routes
from flask import Flask, render_template, request, redirect
from flaskapp import app  # importing the flask app from our package defined in __init__.py
from flaskapp import db
from flaskapp.models import publicAccount, adminAccount
import sqlalchemy as sa
# old datastore code:
# from google.cloud import datastore
# from google.cloud.datastore.query import And, PropertyFilter
# datastore_client = datastore.Client()

ACCOUNTS = "accounts"
ADMINS = "administrator"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'phoneNumber', 'password']
# Error Message
ERROR_MISSING_VALUE = "Not all required values were provided"
ERROR_NOT_FOUND_ACC = "The requested account was not found"


@app.route("/")
def root():
    return render_template("index.html", title="Front end not yet implemented")

# -------------------------------------------------------- Public Account

# Create Public Account
@app.route('/' + ACCOUNTS, methods=['POST'])
def createPublicAccount():
    if request.method == 'POST': # add account
        content = request.get_json()
        # check  if minimum info was provided
        if not (set(MIN_ACCOUNT).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_account = publicAccount(firstName=content['firstName'],
                                    lastName=content['lastName'],
                                    email=content['email'],
                                    phoneNumber=content['phoneNumber'],
                                    password=content['password'])
        db.session.add(new_account) # INSERT
        db.session.commit()
        return "Account was successfully created!", 201


@app.route('/' + ACCOUNTS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def PublicAccountFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(publicAccount).where(publicAccount.idPublicAccounts == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("account.html", title="My Account", results=accounts), 200
    if request.method == 'DELETE':
        query = sa.delete(publicAccount).where(publicAccount.idPublicAccounts == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)
    if request.method == 'PUT':
        content = request.get_json()
        if 'firstName' in content:
            query = sa.update(publicAccount).where(publicAccount.idPublicAccounts == id).values(firstName=content['firstName'])
            db.session.execute(query)
            db.session.commit()
        if 'lastName' in content:
            query = sa.update(publicAccount).where(publicAccount.idPublicAccounts == id).values(lastName=content['lastName'])
            db.session.execute(query)
            db.session.commit()
        if 'email' in content:
            query = sa.update(publicAccount).where(publicAccount.idPublicAccounts == id).values(email=content['email'])
            db.session.execute(query)
            db.session.commit()
        if 'phoneNumber' in content:
            query = sa.update(publicAccount).where(publicAccount.idPublicAccounts == id).values(phoneNumber=content['phoneNumber'])
            db.session.execute(query)
            db.session.commit()
        if 'password' in content:
            query = sa.update(publicAccount).where(publicAccount.idPublicAccounts == id).values(password=content['password'])
            db.session.execute(query)
            db.session.commit()
        return "Account was successfully updated!", 201


# -------------------------------------------------------- Admin Account

# Create Admin Account
@app.route('/' + ADMINS, methods=['POST'])
def createAdminAccount():
    if request.method == 'POST':  # add account
        content = request.get_json()
        # check  if minimum info was provided
        if not (set(MIN_ACCOUNT).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_account = adminAccount(firstName=content['firstName'],
                                   lastName=content['lastName'],
                                   email=content['email'],
                                   phoneNumber=content['phoneNumber'],
                                   password=content['password'])
        db.session.add(new_account)  # INSERT
        db.session.commit()
        return "Account was successfully created!", 201
    
@app.route('/' + ADMINS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def AdminAccountFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(adminAccount).where(adminAccount.idAdminAccounts == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("administratoraccount.html", title="Admin Account", results=accounts), 200
    if request.method == 'DELETE':
        query = sa.delete(adminAccount).where(adminAccount.idAdminAccounts == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)
    if request.method == 'PUT':
        content = request.get_json()
        if 'firstName' in content:
            query = sa.update(adminAccount).where(adminAccount.idAdminAccounts == id).values(firstName=content['firstName'])
            db.session.execute(query)
            db.session.commit()
        if 'lastName' in content:
            query = sa.update(adminAccount).where(adminAccount.idAdminAccounts == id).values(lastName=content['lastName'])
            db.session.execute(query)
            db.session.commit()
        if 'email' in content:
            query = sa.update(adminAccount).where(adminAccount.idAdminAccounts == id).values(email=content['email'])
            db.session.execute(query)
            db.session.commit()
        if 'phoneNumber' in content:
            query = sa.update(adminAccount).where(adminAccount.idAdminAccounts == id).values(phoneNumber=content['phoneNumber'])
            db.session.execute(query)
            db.session.commit()
        if 'password' in content:
            query = sa.update(adminAccount).where(adminAccount.idAdminAccounts == id).values(password=content['password'])
            db.session.execute(query)
            db.session.commit()
        return "Account was successfully updated!", 201
        