"""A simple web application using the SQLAlchemy ORM."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from model import DB_DSN
from sqlalchemy import Column, Integer, Text, CheckConstraint, DateTime, func
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

DB_DSN = 'postgresql:///orm_demo'

app = Flask("ORMDemo")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_DSN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# MODELS
class User(db.Model):
    """Represents an account."""

    __tablename__ = 'person'  # class is User, table is named person

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)
    email = Column(
        Text,
        CheckConstraint("email != ''", "empty_user_email"),
        nullable=False,
        unique=True,
    )
    posts = relationship('UserPost', back_populates="user")


class UserPost(db.Model):
    """A blog posting by a user."""

    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    body = Column(Text(), nullable=False)
    user_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    user = relationship(User, back_populates="posts")


# ROUTES
@app.route('/')
def index():
    return "yo"


@app.route('/posts')
def posts():
    ret = ""
    for post in UserPost.query.all():
        ret += f"User: {post.user.name}, post ID: {post.id}\n<br/>"
    return ret

app.run(debug=True)
