import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), unique=False, nullable=False)
    birthdate = Column(Date, nullable=False)
    is_active = Column(Boolean(), unique=False, nullable=False)
    profile = relationship('Profile', backref='user', uselist=False)
    
class Profile(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    about_me = Column(String(250), unique=True, nullable=False)
    image = Column(String(240), nullable=True)
    favorite_games = Column(String(50), unique=False, nullable=False)
    region = Column(String(50), unique=False, nullable=False)
    contact = Column(String(50), unique=True, nullable=False)
    post_id = relationship('Post_user', backref='post', lazy=True)
    profile_comments = relationship('Comment', backref='profile_comment', lazy=True)

class Post_user(Base):
    id = Column(Integer, primary_key=True)
    post_title = Column(String(150), unique=True, nullable=False)
    post_game = Column(String(150))
    post_description = Column(String(400), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('profile.id'))
    post_comments = relationship('Comment', backref='post_comment', lazy=True)
    likes = relationship("PostLike", backref = "post")

class PostLike(Base):
    __tablename__ = 'post_like'
    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey('profile.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

class Comment(Base):
    id = Column(Integer, primary_key=True)
    comment_content = Column(String(400))
    author_id = Column(Integer, ForeignKey("profile.id"))
    post_id = Column(Integer, ForeignKey("post_user.id"))

class Friends(Base):
    __tablename__ = 'Friends'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey("user.id"))
    user_to_id = Column(Integer, ForeignKey("user.id"))

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e