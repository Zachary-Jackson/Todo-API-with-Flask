from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, ValidationError, Length,
                                EqualTo)

from models import User


def user_exists(form, field):
    """This checks the database to see if a user already exists
    in the database. If so a ValidationError is raised."""
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('A User with that username already exists.')


class RegisterForm(FlaskForm):
    """This is the form users use to register."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=4),
            user_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    """This is the form that user's login with."""
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
