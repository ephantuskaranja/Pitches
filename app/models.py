from . import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    pitches = db.relationship('Content', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic')



    def __repr__(self):
        return f'User{self.username}'

    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    pitches = db.relationship('Content', backref='category', lazy='dynamic')

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls):
        categories = Category.query.all()
        return categories


class Content(db.Model):
    __tablename__ = 'pitches'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='pitch', lazy='dynamic')
    votes = db.relationship('Vote', backref='content', lazy='dynamic')


    def save_content(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls, category_id):
        pitches = Content.query.order_by(Content.id.desc()).filter_by(category_id=category_id).all()

        return pitches


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    content_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, content_id):
        comments = Comment.query.order_by(Comment.id.desc()).filter_by(content_id=content_id).all()

        return comments


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))
    vote_number = db.Column(db.Integer)

    def save_vote(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_votes(cls,user_id,content_id):
        votes = Vote.query.filter_by(user_id=user_id,content_id=content_id).all()
        return votes

    @classmethod
    def num_vote(cls,content_id):
        found_votes = db.session.query(func.sum(Vote.vote_number))
        found_votes = found_votes.filter_by(content_id=content_id).group_by(Vote.content_id)
        votes_list = sum([i[0] for i in found_votes.all()])
        return votes_list