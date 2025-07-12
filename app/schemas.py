from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel): # Base schema for Post
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase): # Post creation schema
    pass

class UserOut(BaseModel): # User output schema
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode to read data from SQLAlchemy models

class Post(PostBase): # Post output schema
    id:int
    created_at: datetime
    owner_id: int  # Foreign key to the User model
    owner:UserOut 
     # Owner of the post, using UserOut schema

    class Config: 
        from_attributes = True

class PostOut(BaseModel): # Output schema for Post
    Post: Post
    votes: int  # Number of votes for the post

    class Config: 
        from_attributes = True


class UserCreate(BaseModel): # User creation schema
    email: EmailStr
    password: str

class UserLogin(BaseModel): # User login schema
    email: EmailStr
    password: str

class Token(BaseModel): # Token schema
    access_token: str
    token_type: str

class TokenData(BaseModel): # Token data schema
    id: Optional[int]  # Optional user ID, can be None if not authenticated


class Vote(BaseModel):  # Vote schema
    Post_id: int  # ID of the post being voted on
    dir: int # Direction of the vote (1 for upvote, 0 for downvote)

