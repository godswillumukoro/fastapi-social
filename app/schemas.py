from pydantic import BaseModel, EmailStr
from datetime import datetime

# Define Pydantic model / schema Requests
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True # default to True

class PostCreate(PostBase):
    pass

# Define Pydantic model / schema Response
class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Users
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # convert sqlalmechy to pydantic model