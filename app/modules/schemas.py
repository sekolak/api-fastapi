from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#response
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

#first user class
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
