# routes
from flask import render_template, request, redirect
from flaskapp import app  # importing the flask app from our package defined in __init__.py
from flaskapp import db
from flaskapp.models import publicAccount, adminAccount, animal, newsPost
import sqlalchemy as sa
from sqlalchemy import inspect

ACCOUNTS = "accounts"
ADMINS = "administrator"
ANIMALS = "animals"
NEWSPOSTS = "newsPosts"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'password']  # optional: phoneNumber
MIN_ANIMAL = ['name', 'type']  # optional or defaulted: breed, disposition, availability, description, numImages
MIN_NEWSPOST = ['title', 'body']  # defaulted: datePublished
# errors
ERROR_MISSING_VALUE = "Not all required values were provided"
ERROR_NOT_FOUND_ACC = "The requested account was not found"
ERROR_NOT_FOUND_ANIMAL = "The requested animal was not found"
ERROR_NOT_FOUND_NEWSPOST = "The requested news post was not found"




@app.route("/")
def root():
    return render_template("index.html", title="Front end not yet implemented")

# -------------------------------------------------------- Public Account

# Create Public Account
@app.route('/' + ACCOUNTS, methods=['POST'])
def createPublicAccount():
    if request.method == 'POST': # add account
        content = request.get_json()
        # check if minimum info was provided
        if not (set(MIN_ACCOUNT).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_account = publicAccount(firstName=content.get('firstName'),  # .get() prevents KeyError for nullables
                                    lastName=content.get('lastName'),
                                    email=content.get('email'),
                                    phoneNumber=content.get('phoneNumber'),
                                    password=content.get('password'))
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
        # check if minimum info was provided
        if not (set(MIN_ACCOUNT).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_account = adminAccount(firstName=content.get('firstName'),
                                   lastName=content.get('lastName'),
                                   email=content.get('email'),
                                   phoneNumber=content.get('phoneNumber'),
                                   password=content.get('password'))
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
        

# -------------------------------------------------------- Animal

# Create Animal
@app.route('/' + ANIMALS, methods=['POST'])
def createAnimal():
    if request.method == 'POST':  # add animal
        content = request.get_json()
        # check if minimum info was provided
        if not (set(MIN_ANIMAL).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_animal = animal(name=content.get('name'),
                            birthday=content.get('birthday'),
                            type=content.get('type'),
                            breed=content.get('breed'),
                            disposition=content.get('disposition'),
                            availability=content.get('availability'),
                            description=content.get('description'),
                            numImages=content.get('numImages')
                            )
        db.session.add(new_animal)  # INSERT
        db.session.commit()
        return "Animal was successfully created!", 201


@app.route('/' + ANIMALS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def animalFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(animal).where(animal.idAnimals == id)
        animals = db.session.execute(query).mappings().all()
        if animals is None:
            return ERROR_NOT_FOUND_ANIMAL, 404
        return render_template("animal.html", title="Animals", results=animals), 200

    if request.method == 'DELETE':
        query = sa.delete(animal).where(animal.idAnimals == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)

    if request.method == 'PUT':
        content = request.get_json()
        # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapper-inspection-mapper
        # https://docs.sqlalchemy.org/en/20/core/dml.html
        table_columns = inspect(animal).columns  # get every type of column from model
        for column in table_columns:
            if content.get(column.name, "") != "":
                query = sa.update(animal).where(animal.idAnimals == id).values({column.name: content[column.name]})
                db.session.execute(query)
                db.session.commit()

        return "Animal was successfully updated!", 201


# -------------------------------------------------------- NewsPost

# Create News Post
@app.route('/' + NEWSPOSTS, methods=['POST'])
def createNewsPost():
    if request.method == 'POST':  # add newsPost
        content = request.get_json()
        # check if minimum info was provided
        if not (set(MIN_NEWSPOST).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_newsPost = newsPost(title=content.get('title'),
                                body=content.get('body'),
                                datePublished=content.get('datePublished')
                                )
        db.session.add(new_newsPost)  # INSERT
        db.session.commit()
        return "News post was successfully created!", 201


@app.route('/' + NEWSPOSTS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def newsPostFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(newsPost).where(newsPost.idNewsPosts == id)
        newsPosts = db.session.execute(query).mappings().all()
        if newsPosts is None:
            return ERROR_NOT_FOUND_NEWSPOST, 404
        return render_template("newsPost.html", title="newsPosts", results=newsPosts), 200

    if request.method == 'DELETE':
        query = sa.delete(newsPost).where(newsPost.idNewsPosts == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)

    if request.method == 'PUT':
        content = request.get_json()

        table_columns = inspect(newsPost).columns
        for column in table_columns:
            if content.get(column.name, "") != "":
                query = sa.update(newsPost).where(newsPost.idNewsPosts == id).values({column.name: content[column.name]})
                db.session.execute(query)
                db.session.commit()

        return "News post was successfully updated!", 201
