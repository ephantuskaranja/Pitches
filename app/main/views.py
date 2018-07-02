from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Category, Content, Comment, Vote
from .forms import CategoryForm, ContentForm, CommentForm
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
    content = Content.query.filter_by(category_id=id)
    print(content)

    title2 = f'{category.name} page'

    return render_template('category.html',title=title2, category=category,content=content)

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
    comment = Comment.get_comments(content_id=id)

    total_votes = Vote.num_vote(content.id)


    title = f'Pitch { content.id }'
    return render_template('show_pitches.html',title=title, content=content,comment=comment,total_votes=total_votes)


@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    pitch = Content.query.get(id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(comment=comment, user=current_user, content_id=id)
        new_comment.save_comment()
        return redirect(url_for('.pitch', id=id))
    # title = f' Comment{comment.id}'
    return render_template('new_comment.html', comment_form=form, content=pitch)


@main.route('/pitch/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    content = Content.query.get(id)

    new_vote = Vote(user=current_user, content=content, vote_number=1)
    new_vote.save_vote()
    return redirect(url_for('.pitch', id=id))


@main.route('/pitch/downvote/<int:id>')
@login_required
def downvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    content = Content.query.get(id)

    new_vote = Vote(user=current_user, content=content, vote_number=-1)
    new_vote.save_vote()
    return redirect(url_for('.pitch', id=id))