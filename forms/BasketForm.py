from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField

class BasketForm(FlaskForm):

    submit = SubmitField('Delete')

