from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(60), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(nullable=False)
    profile_picture = Column(String(300))
    bio = Column(Text)
    is_active = Column(Boolean(), nullable=False)

    post = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    media = relationship("Media", back_populates="user")

    followers = relationship(
        "Follower",
        foreign_keys="Follower.followed_id",
        back_populates="followed"
    )
    following = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower"
    )


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(300), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    media = relationship("Media", back_populates="post")


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(200), nullable=True)
    url = Column(String(300),)
    post_id = Column(Integer, ForeignKey('post.id'))

    post = relationship("Post", back_populates="media")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followed_id = Column(Integer, ForeignKey('user.id'))

    follower = relationship("User", foreign_keys=[
                            follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[
                            followed_id], back_populates="followers")


try:
    result = render_er(Base, 'diagram.png')
    print("¡Diagrama generado exitosamente! Mira el archivo diagram.png")
except Exception as e:
    print("Error al generar el diagrama:", e)
