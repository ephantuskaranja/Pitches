from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required


class CategoryForm(FlaskForm):
    """
    class to create a form to create category
    """
    name = StringField('Pitch Category',validators=[Required()])
    submit = SubmitField('Create')


class ContentForm(FlaskForm):
    """
    class to create form to write pitches
    """
    pitch = StringField('Pitch Content', validators=[Required()])
    submit = SubmitField('Submit')
