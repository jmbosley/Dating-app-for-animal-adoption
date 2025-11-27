# routes
import os
from flask import render_template, request, redirect, url_for, flash
from flaskapp import app, login_manager  # importing the flask app from our package defined in __init__.py
from flaskapp import db
from flaskapp.models import user, animal, newsPost
import sqlalchemy as sa
from sqlalchemy import inspect, func
from flaskapp.forms import (createAnimalForm, updateAccountForm, createAccountForm, deleteButton,
                             editAnimalForm, LoginForm, createNewsPostForm, editNewsPostForm)
from PIL import Image
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

from flask_bcrypt import Bcrypt


ACCOUNTS = "accounts"
ADMINS = "administrator"
ANIMALS = "animals"
NEWSPOSTS = "newsPosts"
MIN_ACCOUNT = ['firstName', 'lastName', 'email', 'password', 'userName']  # optional: phoneNumber
MIN_ANIMAL = ['name', 'type', 'children', 'dogs', 'cats', 'needsLeash']  # optional or defaulted: breed, availability, description, numImages
MIN_NEWSPOST = ['title', 'body']  # idAnimal, datePublished
bcrypt = Bcrypt()

# errors
ERROR_FORM = "Form returned an error"
ERROR_MISSING_VALUE = "Not all required values were provided"
ERROR_NOT_FOUND_ACC = "The requested account was not found"
ERROR_NOT_FOUND_ANIMAL = "The requested animal was not found"
ERROR_NOT_FOUND_NEWSPOST = "The requested news post was not found"
ERROR_UNAUTHORIZED = "You are not authorized to perform this action"


#admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


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
        if content.get(column.name, "") not in ("", None) or column.nullable:
            # print(column.name, content[column.name])
            query = sa.update(model_type).where(model_type.id == id).values({column.name: content[column.name]})
            db.session.execute(query)
            db.session.commit()

def prefillEditForm(form, entity):
    """
    Takes a form and an entity.
    Fills that form according to entity's attributes.
    """
    for field in form:
        try:
            field_name = field.name
            # https://stackoverflow.com/questions/31423495/how-to-dynamically-set-default-value-in-wtforms-radiofield
            field.default = getattr(entity, field_name)  # entity.field_name
        except AttributeError:
            continue
    form.process()


# -------------------------------------------------------- Authentication Routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))
    
    form = LoginForm()
    if form.validate_on_submit():
        #find user by username
        user_obj = user.query.filter_by(userName=form.userName.data).first()
        
        if user_obj is None:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        #check password using the existing password field
        if not bcrypt.check_password_hash(user_obj.password, form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        #Log  user in
        login_user(user_obj, remember=form.remember.data)
        
        #flash different messages based on admin status so you can tell if you are admin
        if user_obj.admin:
            flash(f'Welcome back, Admin {user_obj.firstName}!', 'success')
        else:
            flash(f'Welcome back, {user_obj.firstName}!', 'success')
        
        # redirect to next page or home
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('root'))
    
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('root'))

# -------------------------------------------------------- Browse Animals Routes

@app.route('/browse')
@login_required
def browse():
    """Browse animals page with filtering"""
    
    #Start with base query
    query = sa.select(animal)
    
    #to apply filters from user
    filters = []
    
    #type filter
    animal_type = request.args.get('type')
    if animal_type:
        filters.append(animal.type == animal_type)
    
    #Breed filter
    breed = request.args.get('breed')
    if breed:
        filters.append(animal.breed == breed)
    
    #Availability filter
    availability = request.args.get('availability')
    if availability:
        filters.append(animal.availability == availability)
    
    #Disposition filters
    if request.args.get('good_with_children') == 'true':
        filters.append(animal.children == True)
    
    if request.args.get('good_with_dogs') == 'true':
        filters.append(animal.dogs == True)
    
    if request.args.get('good_with_cats') == 'true':
        filters.append(animal.cats == True)
    
    if request.args.get('needs_leash') == 'true':
        filters.append(animal.needsLeash == True)
    
    # Apply all filters
    if filters:
        query = query.where(sa.and_(*filters))
    
    # Apply our sorting
    sort_by = request.args.get('sort', 'newest')
    if sort_by == 'oldest':
        query = query.order_by(animal.id.asc())
    elif sort_by == 'name':
        query = query.order_by(animal.name.asc())
    else:  #sort by newest as default
        query = query.order_by(animal.id.desc())
    
    #executes query
    animals = db.session.execute(query).scalars().all()
    
    return render_template('browse.html', animals=animals)

# -------------------------------------------------------- Public Routes

@app.route("/")
def root():
    return render_template("index.html", title="Animal Adoption Dating Site")



# -------------------------------------------------------- Public Account

def saveAccountImages(images, user):
    # delete old images
    for img in range(0, user.numImages):
        old_filename = f"accountImg_{user.userName}_{img}.jpg"
        old_filepath = os.path.join(app.root_path, "static/images/user_images", old_filename)
        if os.path.exists(old_filepath):
            os.remove(old_filepath)

    # add new images
    for img in range(0, len(images)):
        curr_img = images[img]

        file_extension = os.path.splitext(curr_img.filename)[1]

        # convert any png to jpg
        if file_extension == '.png':
            curr_img = Image.open(curr_img)  # convert with Pillow
            curr_img = curr_img.convert('RGB')
            file_extension = '.jpg'

        new_filename = f"accountImg_{user.userName}{file_extension}"
        new_filepath = os.path.join(app.root_path, "static/images/user_images", new_filename)

        curr_img.save(new_filepath)
    return


# Create Public Account
@app.route('/' + ACCOUNTS, methods=['GET', 'POST'])
def createuser():
    form = createAccountForm()

    if request.method == 'GET':
        
        return render_template('createAccount.html', title='Create Account', form=form)

    if request.method == 'POST':  # add Account
        if form.validate_on_submit():
            content = form.data
            password_hash = bcrypt.generate_password_hash(content.get('password')).decode('utf-8')
            new_account = user(
                                firstName=content.get('firstName'),
                                lastName=content.get('lastName'),
                                userName=content.get('userName'),
                                password=password_hash,
                                email=content.get('email'),
                                phoneNumber=content.get('phoneNumber'),
                                numImages=0,
                                admin=False
                                )

            db.session.add(new_account)  # INSERT
            db.session.commit()

            # empty image upload returns this: [<FileStorage: '' ('application/octet-stream')>]
            num_images = len(content.get('images', []))
            # add pictures
            if num_images != 0 and content['images'][0].filename != '':
                saveAccountImages(content['images'], new_account)
                query = sa.update(user).where(user.id == new_account.id).values({'numImages': num_images})
                db.session.execute(query)
                db.session.commit()

            flash('Account created successfully!', 'success')
            
            # Auto-login if not already logged in
            if not current_user.is_authenticated:
                login_user(new_account)
                
            return redirect('/' + ACCOUNTS + '/' + str(new_account.id))
        else:
            return render_template('createAccount.html', title='Create Account', form=form)


@app.route('/' + ACCOUNTS + '/<int:id>', methods=['GET', 'DELETE', 'PUT', 'POST'])
@login_required
def userFunctions(id):
    form = updateAccountForm()
    
    # Check if user can access this account (own account or admin)
    if current_user.id != id and not current_user.admin:
        flash('You can only view/edit your own account.', 'danger')
        return redirect(url_for('userFunctions', id=current_user.id))

    if request.method == 'GET':  # display page
        query = sa.select(user).where(user.id == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("account.html", title="My Account", results=accounts), 200
    if request.method == 'DELETE':
        # Only admin can delete accounts
        if not current_user.admin:
            return ERROR_UNAUTHORIZED, 403
        else:
            query = sa.delete(user).where(user.id == id)
            db.session.execute(query)
            db.session.commit()
            return ('', 204)
    if request.method == 'POST':
        content = form.data
        print(content)
        curr_method = request.form["_method"]
        if curr_method == "PUT":
            if form.firstName.data:
                query = sa.update(user).where(user.id == id).values(firstName=content['firstName'])
                db.session.execute(query)
                db.session.commit()
            if form.lastName.data:
                query = sa.update(user).where(user.id == id).values(lastName=content['lastName'])
                db.session.execute(query)
                db.session.commit()
            if form.email.data:
                query = sa.update(user).where(user.id == id).values(email=content['email'])
                db.session.execute(query)
                db.session.commit()
            if form.phoneNumber.data:
                query = sa.update(user).where(user.id == id).values(phoneNumber=content['phoneNumber'])
                db.session.execute(query)
                db.session.commit()

            query = sa.select(user).where(user.id == id)
            accounts = db.session.execute(query).scalars().one()

            num_images = len(content.get('images', []))
            # add pictures
            if num_images != 0 and content['images'][0].filename != '':
                saveAccountImages(content['images'], accounts)
                query = sa.update(user).where(user.id == accounts.id).values({'numImages': num_images})
                db.session.execute(query)
                db.session.commit()
            
            flash('Account updated successfully!', 'success')
            return redirect('/' + ACCOUNTS + '/' + str(id))
        else:
            return ERROR_FORM


@app.route('/' + "edit/" + ACCOUNTS + '/<int:id>', methods=['GET'])
@login_required
def userEdit(id):
    #checks if user can edit this account (own account or admin)
    if current_user.id != id and not current_user.admin:
        flash('You can only edit your own account.', 'danger')
        return redirect(url_for('userFunctions', id=current_user.id))
    
    form = updateAccountForm()

    if request.method == 'GET':  # display page
        query = sa.select(user).where(user.id == id)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("editAccount.html", title="My Account", results=accounts, form=form), 200


# -------------------------------------------------------- Admin Pages
@app.route('/' + 'view' + ACCOUNTS, methods=['GET'])
@admin_required
def displayAccounts():
    if request.method == 'GET':  # display page
        query = sa.select(user)
        accounts = db.session.execute(query).mappings().all()
        if accounts is None:
            return ERROR_NOT_FOUND_ACC, 404
        return render_template("viewAccounts.html", title="My Account", results=accounts), 200


@app.route('/' + 'delete' + '/<int:id>', methods=['GET'])
@admin_required
def deleteUser(id):
    query = sa.delete(user).where(user.id == id)
    db.session.execute(query)
    db.session.commit()
    return redirect(url_for('displayAccounts'))


@app.route('/' + 'changeadmin' + '/<int:id>', methods=['GET'])
@admin_required
def changeAdmin(id):
    query = sa.select(user).where(user.id == id)
    adminValue = db.session.execute(query).mappings().all()[0]['user'].admin
    if adminValue:
        query = sa.update(user).where(user.id == id).values(admin=False)
        db.session.execute(query)
        db.session.commit()
        return redirect(url_for('displayAccounts'))
    else:
        query = sa.update(user).where(user.id == id).values(admin=True)
        db.session.execute(query)
        db.session.commit()
        return redirect(url_for('displayAccounts'))



# -------------------------------------------------------- Animal


def deleteImages(animal):
    for img in range(0, animal.numImages):  # needs to be tested when edit animal page is done
        # assumes all saved images are .jpg
        old_filename = f"animalImg_{animal.id}_{img}.jpg"
        old_filepath = os.path.join(app.root_path, "static/images/animalImages", old_filename)
        if os.path.exists(old_filepath):
            os.remove(old_filepath)


# https://www.youtube.com/watch?v=803Ei2Sq-Zs&t=568s
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
def saveImages(images, animal):
    """
    Takes a list of FileStorage images and an animal entity.
    Converts all .png files to .jpg.
    Updates the entity's numImages and its images in images/animalImages.
    """
    # delete old images
    deleteImages(animal)

    # add new images
    for img in range(0, len(images)):
        curr_img = images[img]
        # file_name = curr_img.filename

        file_name = os.path.splitext(curr_img.filename)[0]
        file_extension = os.path.splitext(curr_img.filename)[1]

        # convert any png to jpg
        if file_extension == '.png':
            curr_img = Image.open(curr_img)  # convert with Pillow
            curr_img = curr_img.convert('RGB')
            file_extension = '.jpg'

        new_filename = f"animalImg_{animal.id}_{img}{file_extension}"
        new_filepath = os.path.join(app.root_path, "static/images/animalImages", new_filename)

        curr_img.save(new_filepath)
    return


def accountChoices():
    """
    Generates user choices for edit animal form
    """
    # select all users id and userName. ordered alphabetically by userName
    # https://stackoverflow.com/a/16573690
    query = sa.select(user.id, user.userName).order_by(func.lower(user.userName))
    all_accounts = db.session.execute(query).mappings().all()
    accountList = [(None, "None")]
    for account in all_accounts:
        # https://rtjom.com/blog/2016/10/using-wtforms-with-selectfield-and-fieldlist/
        accountList.append((account["id"], account["userName"]))
    return accountList


# Create Animal
@app.route('/' + ANIMALS, methods=['GET', 'POST'])
@admin_required
def createAnimal():
    form = createAnimalForm()

    if request.method == 'GET':
        return render_template('createAnimal.html', title='Create Animal', form=form)

    if request.method == 'POST':  # add animal
        if form.validate_on_submit() is False:
            return render_template('createAnimal.html', title='Create Animal', form=form)

        content = form.data
        content['breed'] = content.get(f'breed{content.get('type')}')        

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
                            needsLeash=content.get('needsLeash'),
                            iduser=content.get('iduser')
                            )

        # check if user exists. probably won't be provided during creation
        if content.get('iduser') is not None:
            if entityExists(user, content.get('iduser')) is False:
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

        return redirect('/' + ANIMALS + '/' + str(new_animal.id))


@app.route('/' + ANIMALS + '/<int:id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def animalFunctions(id):
    del_form = deleteButton()
    edit_form = editAnimalForm()

    if entityExists(animal, id) is False:
        return ERROR_NOT_FOUND_ANIMAL, 400

    if request.method == 'GET':  # display page
        query = sa.select(animal).where(animal.id == id)
        animals = db.session.execute(query).mappings().all()
        curr_animal = animals[0]['animal']

        return render_template("animal.html", title=f"Pet Profile: {curr_animal.name}", curr_animal=curr_animal, form=del_form), 200

    if request.method == 'POST':
        if not current_user.is_authenticated or not current_user.admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('login'))
   
        curr_method = request.form['_method']

        if curr_method == 'DELETE':
            form = del_form
            if form.validate_on_submit() is False:
                return redirect('/' + ANIMALS + '/' + str(id))

            # delete any animalImages
            query = sa.select(animal).where(animal.id == id)
            animals = db.session.execute(query).mappings().all()
            if animals is None:
                return ERROR_NOT_FOUND_ANIMAL, 404
            curr_animal = animals[0]['animal']
            deleteImages(curr_animal)

            query = sa.delete(animal).where(animal.id == id)
            db.session.execute(query)
            db.session.commit()
            return redirect('/')

        if curr_method == 'PUT':
            form = edit_form
            # update dynamic choices
            form.iduser.choices = accountChoices()
            content = form.data
            # set breed from the correct select
            content['breed'] = content.get(f'breed{content.get('type')}')   

            if form.validate_on_submit() is False:
                # print(form.errors.items())
                return redirect('/' + "edit/" + ANIMALS + '/' + str(id))

            if content.get('iduser'): # if not falsy: "" or None
                # check if user exists if one was provided
                if entityExists(user, content.get('iduser')) is False:
                    return ERROR_NOT_FOUND_ACC, 400

            updateEntity(animal, content, id)

            # select animal we're updating
            query = sa.select(animal).where(animal.id == id)
            curr_animal = db.session.execute(query).mappings().all()
            curr_animal = curr_animal[0]['animal']

            # empty image upload returns this: [<FileStorage: '' ('application/octet-stream')>]
            num_images = len(content.get('images', []))
            # add pictures
            if num_images != 0 and content['images'][0].filename != '':
                saveImages(content['images'], curr_animal)
                query = sa.update(animal).where(animal.id == id).values({'numImages': num_images})
                db.session.execute(query)
                db.session.commit()

            return redirect('/' + ANIMALS + '/' + str(id))


@app.route('/' + "edit/" + ANIMALS + '/<int:id>', methods=['GET'])
@admin_required
def AnimalEdit(id):
    form = editAnimalForm()

    if entityExists(animal, id) is False:
        return ERROR_NOT_FOUND_ANIMAL, 400

    if request.method == 'GET':  # display page
        query = sa.select(animal).where(animal.id == id)
        # select animal
        curr_animal = db.session.execute(query).mappings().all()
        curr_animal = curr_animal[0]['animal']

        form.iduser.choices = accountChoices()
        prefillEditForm(form, curr_animal)

        # breed select field changes depending on type
        breed_field = getattr(form, f'breed{curr_animal.type}')  
        breed_field.default = curr_animal.breed
        form.process()

        return render_template("editAnimal.html", title="Edit Animal", curr_animal=curr_animal, form=form), 200


# -------------------------------------------------------- NewsPost

def animalChoices():
    """
    Generates animal choices for forms
    """
    query = sa.select(animal.id, animal.name).order_by(animal.id)
    all_animals = db.session.execute(query).mappings().all()
    animalList = [(None, "None")]
    for curr_animal in all_animals:
        animalList.append((curr_animal["id"], f"{curr_animal['id']}: {curr_animal['name']}"))
    return animalList


# Create News Post
@app.route('/' + NEWSPOSTS, methods=['GET', 'POST'])
@admin_required
def createNewsPost():
    form = createNewsPostForm()
    form.idAnimal.choices = animalChoices()

    if request.method == 'GET':
        form.idAnimal.default = request.args.get('idAnimal')  # ?idAnimal=int
        form.process()
        return render_template('createNewsPost.html', title='Create News Post', form=form)

    if request.method == 'POST':  # add newsPost
        if form.validate_on_submit() is False:
            return render_template('createNewsPost.html', title='Create News Post', form=form)

        content = form.data

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
        return redirect('/' + NEWSPOSTS + '/' + str(new_newsPost.id))


@app.route('/' + NEWSPOSTS + '/<int:id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def newsPostFunctions(id):
    del_form = deleteButton()
    edit_form = editNewsPostForm()
    edit_form.idAnimal.choices = animalChoices()

    if entityExists(newsPost, id) is False:
        return ERROR_NOT_FOUND_NEWSPOST, 400

    if request.method == 'GET':  # display page
        form = del_form
        query = sa.select(newsPost).where(newsPost.id == id)
        curr_newsPost = db.session.execute(query).mappings().all()
        if curr_newsPost is None:
            return ERROR_NOT_FOUND_NEWSPOST, 404
        curr_newsPost = curr_newsPost[0]['newsPost']
        return render_template("newsPost.html", title=f"News Post: {curr_newsPost.title}", curr_newsPost=curr_newsPost, form=form), 200

    if request.method == 'POST':
        if not current_user.is_authenticated or not current_user.admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('login'))

        curr_method = request.form['_method']

        if curr_method == 'PUT':
            form = edit_form
            if form.validate_on_submit() is False:
                return render_template('createNewsPost.html', title='Create News Post', form=form)

            content = form.data

            if content.get('idAnimal'): # if not falsy: "" or None
                # check if animal exists if one was provided
                if entityExists(animal, content.get('idAnimal')) is False:
                    return ERROR_NOT_FOUND_ANIMAL, 400

            # check if minimum info was provided
            if not (set(MIN_NEWSPOST).issubset(content)):
                return ERROR_MISSING_VALUE, 400

            updateEntity(newsPost, content, id)
            return redirect('/' + NEWSPOSTS + '/' + str(id))

        if curr_method == 'DELETE':
            query = sa.delete(newsPost).where(newsPost.id == id)
            db.session.execute(query)
            db.session.commit()
            return redirect('/')         


@app.route('/' + "edit/" + NEWSPOSTS + '/<int:id>', methods=['GET'])
@admin_required
def newsPostEdit(id):
    form = editNewsPostForm()

    if entityExists(newsPost, id) is False:
        return ERROR_NOT_FOUND_NEWSPOST, 400

    if request.method == 'GET':  # display page
        query = sa.select(newsPost).where(newsPost.id == id)
        # select newsPost
        curr_newsPost = db.session.execute(query).mappings().all()
        if curr_newsPost is None:
            return ERROR_NOT_FOUND_NEWSPOST, 404
        curr_newsPost = curr_newsPost[0]['newsPost']

        form.idAnimal.choices = animalChoices()
        prefillEditForm(form, curr_newsPost)

        return render_template("editNewsPost.html", title="Edit News Post", curr_newsPost=curr_newsPost, form=form), 200


# Context processor to make current_user available in all templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)