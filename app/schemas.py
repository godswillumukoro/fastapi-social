from pydantic import BaseModel
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
        orm_mode = True