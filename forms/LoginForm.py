from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField

class LoginForm(FlaskForm):

    userName = StringField('Email')
    passW = StringField('Password')
    submit = SubmitField('Login')


