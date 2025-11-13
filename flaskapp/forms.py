import os
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, MultipleFileField,
                     DateField, SelectField, TextAreaField, IntegerField, FileField)
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from flaskapp.models import publicAccount, adminAccount, animal, newsPost


ANIMAL_TYPES = ["Dog", "Cat", "Bird", "Bunny", "Ferret", "Rat", "Mouse", "Chinchilla", "Other"]
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
    user = publicAccount.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('email already exists')

def validate_username(self, userName):
    user = publicAccount.query.filter_by(userName=userName.data).first()
    if user:
        raise ValidationError('userName already exists')

def coerceIntSelect(input):
    if input in ["None", None]:  # SelectFields will convert None to str, convert back
        return None
    return int(input)


class createAnimalForm(FlaskForm):
    # field = fieldType('labelname', validators=[])
    availability = SelectField('Availability', validators=[DataRequired()], choices=AVAILABILITY_TYPES)

    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=45)])
    birthday = DateField('Birthday', validators=[Optional()])
    type = SelectField('Type', validators=[DataRequired()], choices=ANIMAL_TYPES)
    breed = StringField('Breed', validators=[Optional(), Length(min=0, max=45)])
    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=1000)])

    children = BooleanField('Good with Children', default=True)
    dogs = BooleanField('Good with Dogs', default=True)
    cats = BooleanField('Good with Cats', default=True)
    needsLeash = BooleanField('Must be leashed at all times', default=False)

    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])

    createNewsPost = BooleanField('Create a news post about this animal\'s arrival', default=False)

    submit = SubmitField('Submit')


class editAnimalForm(FlaskForm):
    # field = fieldType('labelname', validators=[])
    availability = SelectField('Availability', validators=[Optional()], choices=AVAILABILITY_TYPES)
    # coerce is passed a function it inputs the selected value into.
    idPublicAccount = SelectField('Owner', validators=[Optional()], choices=[], coerce=coerceIntSelect)

    name = StringField('Name', validators=[Optional(), Length(min=1, max=45)])
    birthday = DateField('Birthday', validators=[Optional()])
    type = SelectField('Type', validators=[Optional()], choices=ANIMAL_TYPES)
    breed = StringField('Breed', validators=[Optional(), Length(min=0, max=45)])
    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=1000)])

    children = BooleanField('Good with Children')
    dogs = BooleanField('Good with Dogs')
    cats = BooleanField('Good with Cats')
    needsLeash = BooleanField('Must be leashed at all times')

    images = MultipleFileField('Replace Images', validators=[validateImages, Optional()])

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
    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])
    submit = SubmitField('Submit')


class deleteButton(FlaskForm):
    delete = SubmitField('Delete')
