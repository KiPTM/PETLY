from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, FloatField, SubmitField  # Add FloatField here
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import os

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import os
class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image_url = FileField('Pet Picture')  # For uploading pet pictures
    submit = SubmitField('Submit')

    def validate_image_url(self, image_url):
        if image_url.data:
            _, ext = os.path.splitext(image_url.data.filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise ValidationError('Invalid file type. Allowed types: jpg, jpeg, png, gif.')
class ProfileForm(FlaskForm):
    profile_picture = FileField('Profile Picture')  # For uploading a profile picture
    bio = TextAreaField('Bio', validators=[Length(max=500)])  # User's bio
    submit = SubmitField('Update Profile')

    def validate_profile_picture(self, profile_picture):
        if profile_picture.data:
            _, ext = os.path.splitext(profile_picture.data.filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise ValidationError('Invalid file type. Allowed types: jpg, jpeg, png, gif.')