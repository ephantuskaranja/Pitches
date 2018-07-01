from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Category, Content
from .forms import CategoryForm, ContentForm
from flask_login import login_required,current_user

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    categories = Category.get_categories()
    title = 'Home'

    return render_template('index.html', title = title ,categories=categories)


@main.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category()
        return redirect(url_for('.index'))
    title = 'New Pitch Category'
    return render_template('new_pitchcategory.html', category_form=form)


#get categories
@main.route('/category/<int:id>')
def category(id):
    category = Category.query.get(id)
    pitch = Content.query.filter_by(category_id=id)


    title2 = f'{category.name} page'

    return render_template('category.html',title=title2, category=category,pitch=pitch)

#add pitches
@main.route('/category/pitch/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    category = Category.query.get(id)
    form = ContentForm()
    if form.validate_on_submit():
        content = form.content.data
        new_content = Content(content=content, user=current_user, category_id=id)
        new_content.save_content()
        return redirect(url_for('.category', id=id))

    title = 'New Pitch'
    return render_template('new_content.html', title=title, content_form=form)

#display pitches
@main.route('/pitch/<int:id>')
def pitch(id):
    content = Content.query.get(id)
    comment = Comment.get_comments(content_id)

    title = f'Pitch { pitch.id }'
    return render_template('show_pitches.html',title=title, content=content,comment=comment)


@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    pitch = Content.query.get(id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(comment=comment, user=current_user, pitch_id=id)
        new_comment.save_comment()
        return redirect(url_for('.pitch', id=id))
    # title = f' Comment{comment.id}'
    return render_template('new_comment.html', comment_form=form, content=pitch)
