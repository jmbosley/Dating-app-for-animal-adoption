import os
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, MultipleFileField,
                     DateField, SelectField, TextAreaField, IntegerField)
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired


TYPES = ["Dog", "Cat", "Bird", "Bunny", "Ferret", "Rat", "Mouse", "Chinchilla"]


def validateImages(form, field):
    # https://wtforms.readthedocs.io/en/2.3.x/validators/
    for file in field.data:
        if len(field.data) == 1 and file.filename == "":
            continue
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension not in [".jpg", ".png"]:
            raise ValidationError("File must be jpg or png")


class createAnimalForm(FlaskForm):
    # field = fieldType('labelname', validators=[])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=45)])
    birthday = DateField('Birthday', validators=[Optional()])
    type = SelectField('Type', validators=[DataRequired()], choices=TYPES)
    breed = StringField('Breed', validators=[Optional(), Length(min=0, max=45)])
    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=300)])

    children = BooleanField('Good with Children', default=True)
    dogs = BooleanField('Good with Dogs', default=True)
    cats = BooleanField('Good with Cats', default=True)

    images = MultipleFileField('Add some Images', validators=[validateImages, Optional()])

    submit = SubmitField('Submit')
