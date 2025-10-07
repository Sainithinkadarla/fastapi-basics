from fastapi import FastAPI, status
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int

class Post(PostBase):
    id: int
    views: int = 0

class Dummy:
    posts: dict[int, Post] = {}


db = Dummy()
app = FastAPI()


@app.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create(post_create: PostCreate):
    new_id = max(db.posts.keys() or (0,)) + 1

    post = Post(id = new_id, **post_create.model_dump())

    db.posts[new_id] = post
    return post

@app.get("/posts")
async def read_all():
    return db.posts


