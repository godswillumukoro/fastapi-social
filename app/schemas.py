from pydantic import BaseModel

# Pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True # default to True

class PostCreate(PostBase):
    pass
