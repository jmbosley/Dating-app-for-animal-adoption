import os
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, MultipleFileField,
                     DateField, SelectField, TextAreaField, IntegerField, FileField)
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from flaskapp.models import user, animal, newsPost


ANIMAL_TYPES = ["Dog", "Cat", "Other"]
DOG_BREEDS = ['Other', 'Afghan Hound', 'Airedale Terrier', 'Akita', 'Alaskan Malamute', 'American Eskimo Dog',
              'American Staffordshire Terrier', 'Anatolian Shepherd Dog', 'Australian Cattle Dog',
              'Australian Shepherd', 'Basenji', 'Basset Hound', 'Beagle', 'Beauceron', 'Belgian Malinois',
              'Belgian Tervuren', 'Bernese Mountain Dog', 'Bichon Frise', 'Biewer Terrier', 'Bloodhound', 'Boerboel',
              'Border Collie', 'Border Terrier', 'Borzoi', 'Boston Terrier', 'Bouvier des Flandres', 'Boxer',
              'Boykin Spaniel', 'Brittany', 'Brussels Griffon', 'Bull Terrier', 'Bulldog', 'Bullmastiffs',
              'Cairn Terrier', 'Cane Corso', 'Cardigan Welsh Corgi', 'Cavalier King Charles Spaniel',
              'Chesapeake Bay Retriever', 'Chihuahua', 'Chinese Crested', 'Chinese Shar-Pei', 'Chow Chow',
              'Cocker Spaniel', 'Collie', 'Coton de Tulear', 'Dachshund', 'Dalmatian', 'Doberman Pinscher',
              'Dogo Argentino', 'Dogue de Bordeaux', 'English Cocker Spaniel', 'English Setter',
              'English Springer Spaniel', 'Flat-Coated Retriever', 'French Bulldog', 'German Shepherd Dog',
              'German Shorthaired Pointer', 'German Wirehaired Pointer', 'Giant Schnauzer', 'Golden Retriever',
              'Gordon Setter', 'Great Dane', 'Great Pyrenees', 'Great Swiss Mountain Dog', 'Greyhound', 'Havanese',
              'Irish Setter', 'Irish Wolfhound', 'Italian Greyhound', 'Japanese Chin', 'Keeshond',
              'Labrador Retriever', 'Lagotto Romagnolo', 'Leonberger', 'Lhasa Apso', 'Maltese',
              'Manchester Terrier', 'Mastiff', 'Miniature American Shepherd', 'Miniature Bull Terrier',
              'Miniature Pinscher', 'Miniature Schnauzer', 'Newfoundland', 'Norwich Terrier',
              'Nova Scotia Duck Tolling Retriever', 'Old English Sheepdog', 'Papillon', 'Parson Russell Terrier',
              'Pekingese', 'Pembroke Welsh Corgi', 'Pomeranian', 'Poodle', 'Portuguese Water Dog', 'Pug',
              'Rat Terrier', 'Rhodesian Ridgeback', 'Rottweiler', 'Russell Terrier', 'Saint Bernard', 'Samoyed',
              'Schipperke', 'Scottish Terrier', 'Shetland Sheepdog', 'Shiba Inu', 'Shih Tzu', 'Siberian Husky',
              'Silky Terrier', 'Soft Coated Wheaten Terrier', 'Staffordshire Bull Terrier', 'Standard Schnauzer',
              'Tibetan Terrier', 'Toy Fox Terrier', 'Vizsla', 'Weimaraner', 'West Highland White Terrier',
              'Whippet', 'Wire Fox Terrier', 'Wirehaired Pointing Griffon', 'Yorkshire Terrier',]
CAT_BREEDS = ['Other', 'Abyssinian', 'Bengal', 'British Shorthair', 'Burmese', 'Devon Rex', 'Domestic Shorthair',
              'Exotic Shorthair', 'Maine Coon', 'Norwegian Forest', 'Persian', 'Ragdoll', 'Russian Blue',
              'Scottish Fold', 'Siamese', 'Sphynx']
OTHER_BREEDS = ["Other"]
AVAILABILITY_TYPES = ["Available", "Not Available", "Pending", "Adopted"]


def validateImages(form, field):
    # https://wtforms.readthedocs.io/en/2.3.x/validators/
    for file in field.data:
        if len(field.data) == 1 and file.filename == "":
            continue
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension not in [".jpg", ".png"]:
            raise ValidationError("File must be jpg or png")


def validate_email(self, email):
    useraccount = user.query.filter_by(email=email.data).first()
    if useraccount:
        raise ValidationError('email already exists')

def validate_username(self, userName):
    useraccount = user.query.filter_by(userName=userName.data).first()
    if useraccount:
        raise ValidationError('userName already exists')

def coerceIntSelect(input):
    if input in ["None", None]:  # SelectFields will convert None to str, convert back
        return None
    return int(input)


class LoginForm(FlaskForm):
    """Form for user login"""
    userName = StringField('Username', validators=[DataRequired(), Length(min=1, max=45)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class createAnimalForm(FlaskForm):
    # field = fieldType('labelname', validators=[])
    availability = SelectField('Availability', validators=[DataRequired()], choices=AVAILABILITY_TYPES)

    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=45)])
    birthday = DateField('Birthday', validators=[Optional()])
    type = SelectField('Type', validators=[DataRequired()], choices=ANIMAL_TYPES, render_kw={'onchange': "breedDisplay(typeChoices)"})
    
    breed = StringField('Breed', validators=[Optional(), Length(min=0, max=45)])
    breedDog = SelectField('Breed', validators=[Optional()], choices=DOG_BREEDS)
    breedCat = SelectField('Breed', validators=[Optional()], choices=CAT_BREEDS)
    breedOther = SelectField('Breed', validators=[Optional()], choices=OTHER_BREEDS)

    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=1000)])

    children = BooleanField('Good with Children', default=True)
    dogs = BooleanField('Good with Dogs', default=True)
    cats = BooleanField('Good with Cats', default=True)
    needsLeash = BooleanField('Must be leashed at all times', default=False)

    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])

    submit = SubmitField('Submit')


class editAnimalForm(FlaskForm):
    # field = fieldType('labelname', validators=[])
    availability = SelectField('Availability', validators=[Optional()], choices=AVAILABILITY_TYPES)
    # coerce is passed a function it inputs the selected value into.
    iduser = SelectField('Owner', validators=[Optional()], choices=[], coerce=coerceIntSelect)

    name = StringField('Name', validators=[Optional(), Length(min=1, max=45)])
    birthday = DateField('Birthday', validators=[Optional()])
    type = SelectField('Type', validators=[Optional()], choices=ANIMAL_TYPES, render_kw={'onchange': "breedDisplay(typeChoices)"})

    breed = StringField('Breed', validators=[Optional(), Length(min=0, max=45)])
    breedDog = SelectField('Breed', validators=[Optional()], choices=DOG_BREEDS)
    breedCat = SelectField('Breed', validators=[Optional()], choices=CAT_BREEDS)
    breedOther = SelectField('Breed', validators=[Optional()], choices=OTHER_BREEDS)

    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=1000)])

    children = BooleanField('Good with Children')
    dogs = BooleanField('Good with Dogs')
    cats = BooleanField('Good with Cats')
    needsLeash = BooleanField('Must be leashed at all times')

    images = MultipleFileField('Replace Images', validators=[validateImages, Optional()])

    submit = SubmitField('Submit')


class createNewsPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=0, max=10000)])
    idAnimal = SelectField('Related Animal', validators=[Optional()], choices=[], coerce=coerceIntSelect)
    submit = SubmitField('Submit')


class editNewsPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=0, max=10000)])
    datePublished = DateField('Date Published', validators=[Optional()])
    idAnimal = SelectField('Related Animal', validators=[Optional()], choices=[], coerce=coerceIntSelect)
    submit = SubmitField('Submit')


class updateAccountForm(FlaskForm):
    firstName = StringField('firstName', validators=[Optional(), Length(min=1, max=45)])
    lastName = StringField('lastName', validators=[Optional(), Length(min=1, max=45)])
    email = StringField('email', validators=[Optional(), Length(min=1, max=45)])
    phoneNumber = StringField('phoneNumber', validators=[Optional(), Length(min=1, max=45)])
    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])
    submit = SubmitField('Submit')


class createAccountForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired(), Length(min=1, max=45)])
    lastName = StringField('lastName', validators=[DataRequired(), Length(min=1, max=45)])
    userName = StringField('userName', validators=[validate_username, Optional(), Length(min=1, max=45)])
    password = StringField('password', validators=[DataRequired(), Length(min=1, max=45)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('email', validators=[DataRequired(), Length(min=1, max=45)])
    phoneNumber = StringField('phoneNumber', validators=[DataRequired(), Length(min=1, max=45)])
    # Admin checkbox - only shown to admins
    admin = BooleanField('Admin Account', default=False)
    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])
    submit = SubmitField('Submit')


class deleteButton(FlaskForm):
    delete = SubmitField('Delete')