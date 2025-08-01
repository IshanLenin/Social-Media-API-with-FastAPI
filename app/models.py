from sqlalchemy import Column, Integer, String, Boolean,text,ForeignKey
from app.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False)
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner=relationship("User", back_populates="posts")  # Establishing a relationship with the User model
    votes = relationship("Vote", back_populates="post")  # Establishing a relationship with the Vote model


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    posts = relationship("Post", back_populates="owner")  # Relationship with Post model
    votes = relationship("Vote", back_populates="user")  # Relationship with Vote model
    phone_number = Column(String, nullable=True)  # Optional phone number field

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    post = relationship("Post", back_populates="votes")  # Establishing a relationship with the Post model
    user = relationship("User", back_populates="votes")  # Establishing a relationship with the User model
