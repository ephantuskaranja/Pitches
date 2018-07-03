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
    content = StringField('Pitch Content', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
    class to create form to comment on a pitch
    """
    comment = StringField('Comment Content', validators=[Required()])
    submit = SubmitField('Submit')


class UpvoteForm(FlaskForm):
    '''
    Class to create a wtf form for upvoting a pitch
    '''
    submit = SubmitField('Upvote')

