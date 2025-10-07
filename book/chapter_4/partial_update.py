from fastapi import FastAPI, status, HTTPException
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

class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


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

@app.patch("/posts/{id}", response_model=PostRead)
async def partial_update(id: int, post_update: PostPartialUpdate):
    try: 
            post_db = db.posts[id]

            updated_fields = post_update.model_dump(exclude_unset=True)
            updated_post = post_db.model_copy(update = updated_fields)

            db.posts[id] = updated_post
            return updated_post

    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)