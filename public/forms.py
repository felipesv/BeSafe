#!/usr/bin/python3
''' Validation Forms '''
from wtforms import *
from wtforms.validators import *
import email_validator


class SignUp(Form):
    """SignUp
    This class validates that the user registration is correct.
    """
    # fields for form
    name = StringField('Your name', [Length(min=4, max=25), Required()])
    email = StringField('Your email', [Required(), Email()])
    password = PasswordField('Password', [Required() , EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password', [Required()])
    route = HiddenField()
    submit = SubmitField('Registrate')


class LogIn(Form):
    """LogIn
    This class validates that the user login is correct.
    """
    # field for form
    email = StringField('Email', [Required()], id="email_log")
    password = PasswordField('Password', [Required()])
    route = HiddenField('route')
    submit = SubmitField('Iniciar sesión')
