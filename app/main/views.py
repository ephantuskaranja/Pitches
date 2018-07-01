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

    title = 'Home'

    return render_template('index.html', title = title )


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
    title = f'{category.name} page'

    return render_template('category.html',title=title, category=category)

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
