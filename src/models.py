from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from eralchemy2 import render_er


Base = declarative_base()

db = SQLAlchemy()

class User(Base):  
    __tablename__ = 'user' 
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    likes = relationship("Like", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Post(Base):  
    __tablename__ = 'post'  
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
  
    comments = relationship("Comment", backref="post")
    likes = relationship("Like", backref="post")

class Comment(Base):  
    __tablename__ = 'comment'   
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

class Like(Base): 
    __tablename__ = 'like'  
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
