#!/usr/bin/python3
''' Validation Forms '''
from wtforms import *
from wtforms.validators import *


class SignUp(Form):
    """SignUp
    This class validates that the user registration is correct.
    """
    # fields for form
    name = StringField('Your name', [Length(min=4, max=25), Required()])
    email = StringField('Your email', [Required()])
    password = PasswordField('Password', [Required() , EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password', [Required()])
    route = HiddenField()
    submit = SubmitField('Registrate')


class LogIn(Form):
    """LogIn
    This class validates that the user login is correct.
    """
    # field for form
    email = StringField('Email', [Required()])
    password = PasswordField('Password', [Required()])
