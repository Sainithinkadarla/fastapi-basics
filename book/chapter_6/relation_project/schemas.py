from datetime import datetime
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

    class Config():
        from_attributes = True

class PostCreate(PostBase):
    pass

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int

class PostRead(PostBase):
    id: int
    comments: list[CommentRead]

class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None 