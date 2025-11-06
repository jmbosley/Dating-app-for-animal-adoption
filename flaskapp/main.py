# routes
import os
from flask import render_template, request, redirect, url_for, flash
from flaskapp import app  # importing the flask app from our package defined in __init__.py
from flaskapp import db
from flaskapp.models import publicAccount, adminAccount, animal, newsPost
import sqlalchemy as sa
from sqlalchemy import inspect
from flaskapp.forms import createAnimalForm, updateAccountForm, createAccountForm


ACCOUNTS = "accounts"
ADMINS = "administrator"
ANIMALS = "animals"
CREATE_ANIMAL = "createanimal"
NEWSPOSTS = "newsPosts"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'password', 'userName']  # optional: phoneNumber
MIN_ANIMAL = ['name', 'type', 'children', 'dogs', 'cats']  # optional or defaulted: breed, availability, description, numImages
MIN_NEWSPOST = ['title', 'body']  # idAnimal, datePublished
# errors
ERROR_FORM = "Form returned an error"
ERROR_MISSING_VALUE = "Not all required values were provided"
ERROR_NOT_FOUND_ACC = "The requested account was not found"
ERROR_NOT_FOUND_ANIMAL = "The requested animal was not found"
ERROR_NOT_FOUND_NEWSPOST = "The requested news post was not found"

def entityExists(model_type, id):
    """
    Takes model_type and id. Returns True if an entity with that id is found.
    """
    query = sa.select(model_type).where(model_type.id == id)
    entity = db.session.execute(query).mappings().all()
    if not entity:  # query returned empty list (falsy)
        return False
    return True
def updateEntity(model_type, content, id):
    """
    Takes model_type, content, and id.
    Updates model_type entity with that id based on content.
    """
    # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapper-inspection-mapper
    # https://docs.sqlalchemy.org/en/20/core/dml.html
    table_columns = inspect(model_type).columns
    for column in table_columns:
        if content.get(column.name, "") != "":
            query = sa.update(model_type).where(model_type.id == id).values({column.name: content[column.name]})
            db.session.execute(query)
            db.session.commit()

@app.route("/")
def root():
    return render_template("index.html", title="Front end not yet implemented")


# -------------------------------------------------------- Public Account
def saveAccountImages(images, publicAccount):
    # delete old images
    for img in range(0, publicAccount.numImages):
        for extension in ['jpg', 'png']:
            old_filename = f"accountImg_{publicAccount.userName}_{img}{extension}"
            old_filepath = os.path.join(app.root_path, "static/images/user_images", old_filename)
            if os.path.exists(old_filepath):
                os.remove()

    # add new images
    for img in range(0, len(images)):
        curr_img = images[img]
        img_name = curr_img.filename

        file_extension = os.path.splitext(img_name)[1]
        new_filename = f"accountImg_{publicAccount.userName}{file_extension}"
        new_filepath = os.path.join(app.root_path, "static/images/user_images", new_filename)

        curr_img.save(new_filepath)
    return

# Create Public Account
@app.route('/' + ACCOUNTS, methods=['GET', 'POST'])
def createPublicAccount():
    form = createAccountForm()

    if request.method == 'GET':
        
        return render_template('createAccount.html', title='Create Account', form=form)

    if request.method == 'POST':  # add Account
        if form.validate_on_submit():
            content = form.data
            # check if minimum info was provided
            new_account = publicAccount(
                                firstName=content.get('firstName'),
                                lastName=content.get('lastName'),
                                userName=content.get('userName'),
                                password=content.get('password'),
                                email=content.get('email'),
                                phoneNumber=content.get('phoneNumber'),
                                numImages=0,
                                )

            db.session.add(new_account)  # INSERT
            db.session.commit()

            # empty image upload returns this: [<FileStorage: '' ('application/octet-stream')>]
            num_images = len(content.get('images', []))
            # add pictures
            if num_images != 0 and content['images'][0].filename != '':
                saveAccountImages(content['images'], new_account)
                query = sa.update(publicAccount).where(publicAccount.id == new_account.id).values({'numImages': num_images})
                db.session.execute(query)
                db.session.commit()

            return redirect('/' + ACCOUNTS + '/' + str(new_account.id))
        else:
            return render_template('createAccount.html', title='Create Account', form=form)


@app.route('/' + ACCOUNTS + '/<int:id>', methods=['GET', 'DELETE', 'PUT', 'POST'])
def PublicAccountFunctions(id):
    form = updateAccountForm()

    if request.method == 'GET':  # display page
        query = sa.select(publicAccount).where(publicAccount.id == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("account.html", title="My Account", results=accounts), 200
    if request.method == 'DELETE':
        query = sa.delete(publicAccount).where(publicAccount.id == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)
    if request.method == 'POST':
        content = form.data
        print(content)
        curr_method = request.form["_method"]
        if curr_method == "PUT":
            if form.firstName.data:
                query = sa.update(publicAccount).where(publicAccount.id == id).values(firstName=content['firstName'])
                db.session.execute(query)
                db.session.commit()
            if form.lastName.data:
                query = sa.update(publicAccount).where(publicAccount.id == id).values(lastName=content['lastName'])
                db.session.execute(query)
                db.session.commit()
            if form.email.data:
                query = sa.update(publicAccount).where(publicAccount.id == id).values(email=content['email'])
                db.session.execute(query)
                db.session.commit()
            if form.phoneNumber.data:
                query = sa.update(publicAccount).where(publicAccount.id == id).values(phoneNumber=content['phoneNumber'])
                db.session.execute(query)
                db.session.commit()
            
            query = sa.select(publicAccount).where(publicAccount.id == id)
            accounts = db.session.execute(query).scalars().one()

            num_images = len(content.get('images', []))
            # add pictures
            if num_images != 0 and content['images'][0].filename != '':
                saveAccountImages(content['images'], accounts)
                query = sa.update(publicAccount).where(publicAccount.id == accounts.id).values({'numImages': num_images})
                db.session.execute(query)
                db.session.commit()
            return redirect('/' + ACCOUNTS + '/' + str(id))
        else:
            return ERROR_FORM
        

@app.route('/' + "edit/" + ACCOUNTS + '/<int:id>', methods=['GET'])
def PublicAccountEdit(id):
    form = updateAccountForm()

    if request.method == 'GET':  # display page
        query = sa.select(publicAccount).where(publicAccount.id == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("editAccount.html", title="My Account", results=accounts, form=form), 200

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
        query = sa.select(adminAccount).where(adminAccount.id == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("administratoraccount.html", title="Admin Account", results=accounts), 200
    if request.method == 'DELETE':
        query = sa.delete(adminAccount).where(adminAccount.id == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)
    if request.method == 'PUT':
        content = request.get_json()
        if 'firstName' in content:
            query = sa.update(adminAccount).where(adminAccount.id == id).values(firstName=content['firstName'])
            db.session.execute(query)
            db.session.commit()
        if 'lastName' in content:
            query = sa.update(adminAccount).where(adminAccount.id == id).values(lastName=content['lastName'])
            db.session.execute(query)
            db.session.commit()
        if 'email' in content:
            query = sa.update(adminAccount).where(adminAccount.id == id).values(email=content['email'])
            db.session.execute(query)
            db.session.commit()
        if 'phoneNumber' in content:
            query = sa.update(adminAccount).where(adminAccount.id == id).values(phoneNumber=content['phoneNumber'])
            db.session.execute(query)
            db.session.commit()
        if 'password' in content:
            query = sa.update(adminAccount).where(adminAccount.id == id).values(password=content['password'])
            db.session.execute(query)
            db.session.commit()
            
        return "Account was successfully updated!", 201


# -------------------------------------------------------- Animal

# https://www.youtube.com/watch?v=803Ei2Sq-Zs&t=568s
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
def saveImages(images, animal):
    # delete old images
    for img in range(0, animal.numImages):  # needs to be tested when edit animal page is done
        for extension in ['jpg', 'png']:
            old_filename = f"animalImg_{animal.id}_{img}{extension}"
            old_filepath = os.path.join(app.root_path, "static/animalImages", old_filename)
            if os.path.exists(old_filepath):
                os.remove()

    # add new images
    for img in range(0, len(images)):
        curr_img = images[img]
        img_name = curr_img.filename

        file_extension = os.path.splitext(img_name)[1]
        new_filename = f"animalImg_{animal.id}_{img}{file_extension}"
        new_filepath = os.path.join(app.root_path, "static/animalImages", new_filename)

        curr_img.save(new_filepath)
    return


# Create Animal
@app.route('/' + CREATE_ANIMAL, methods=['GET', 'POST'])
def createAnimal():
    form = createAnimalForm()

    if request.method == 'GET':
        return render_template('createAnimal.html', title='Create Animal', form=form)

    if request.method == 'POST':  # add animal
        if form.validate_on_submit() is False:
            return render_template('createAnimal.html', title='Create Animal', form=form)

        content = form.data
        # check if minimum info was provided
        if not (set(MIN_ANIMAL).issubset(content)):
            return ERROR_MISSING_VALUE, 400
        new_animal = animal(name=content.get('name'),
                            birthday=content.get('birthday'),
                            type=content.get('type'),
                            breed=content.get('breed'),
                            availability=content.get('availability'),
                            description=content.get('description'),
                            numImages=0,
                            children=content.get('children'),
                            dogs=content.get('dogs'),
                            cats=content.get('cats'),
                            idPublicAccount=content.get('idPublicAccount')
                            )

        # check if publicAccount exists. probably won't be provided during creation
        if content.get('idPublicAccount') is not None:
            if entityExists(publicAccount, content.get('idPublicAccount')) is False:
                return ERROR_NOT_FOUND_ACC, 400

        # add now because we need the primary key for image naming
        db.session.add(new_animal)  # INSERT
        db.session.commit()

        # empty image upload returns this: [<FileStorage: '' ('application/octet-stream')>]
        num_images = len(content.get('images', []))
        # add pictures
        if num_images != 0 and content['images'][0].filename != '':
            saveImages(content['images'], new_animal)
            query = sa.update(animal).where(animal.id == new_animal.id).values({'numImages': num_images})
            db.session.execute(query)
            db.session.commit()

        return "Animal was successfully created!", 201


@app.route('/' + ANIMALS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def animalFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(animal).where(animal.id == id)
        animals = db.session.execute(query).mappings().all()
        if animals is None:
            return ERROR_NOT_FOUND_ANIMAL, 404
        return render_template("animal.html", title="Animals", results=animals), 200

    if request.method == 'DELETE':
        query = sa.delete(animal).where(animal.id == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)

    if request.method == 'PUT':
        content = request.get_json()

        if content.get('idPublicAccount') is not None:
            # check if publicAccount exists
            if entityExists(publicAccount, content.get('idPublicAccount')) is False:
                return ERROR_NOT_FOUND_ACC, 400

        updateEntity(animal, content, id)

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
                                datePublished=content.get('datePublished'),
                                idAnimal=content.get('idAnimal')
                                )

        if content.get('idAnimal') is not None:
            # check if animal exists
            if entityExists(animal, content.get('idAnimal')) is False:
                return ERROR_NOT_FOUND_ANIMAL, 400

        db.session.add(new_newsPost)  # INSERT
        db.session.commit()
        return "News post was successfully created!", 201


@app.route('/' + NEWSPOSTS + '/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def newsPostFunctions(id):
    if request.method == 'GET':  # display page
        query = sa.select(newsPost).where(newsPost.id == id)
        newsPosts = db.session.execute(query).mappings().all()
        if newsPosts is None:
            return ERROR_NOT_FOUND_NEWSPOST, 404
        return render_template("newsPost.html", title="newsPosts", results=newsPosts), 200

    if request.method == 'DELETE':
        query = sa.delete(newsPost).where(newsPost.id == id)
        db.session.execute(query)
        db.session.commit()
        return ('', 204)

    if request.method == 'PUT':
        content = request.get_json()

        if content.get('idAnimal') is not None:
            # check if animal exists
            if entityExists(animal, content.get('idAnimal')) is False:
                return ERROR_NOT_FOUND_ANIMAL, 400

        updateEntity(newsPost, content, id)

        return "News post was successfully updated!", 201
