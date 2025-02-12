from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SubmitField
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

class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])  # Changed to StringField for simplicity
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):  # Ensure this class exists
    profile_picture = FileField('Profile Picture')  # For uploading a profile picture
    bio = TextAreaField('Bio', validators=[Length(max=500)])  # User's bio
    submit = SubmitField('Update Profile')

    def validate_profile_picture(self, profile_picture):
        if profile_picture.data:
            _, ext = os.path.splitext(profile_picture.data.filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise ValidationError('Invalid file type. Allowed types: jpg, jpeg, png, gif.')
            
