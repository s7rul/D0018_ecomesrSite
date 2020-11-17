from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField

class AddForm(FlaskForm):

    addNumber = StringField('Purchase')
    submit = SubmitField('Add to Cart')



