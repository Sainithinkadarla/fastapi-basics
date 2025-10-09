from fastapi import FastAPI, status, HTTPException, Depends
from contextlib import asynccontextmanager

from project.schemas import PostCreate, PostPartialUpdate, PostRead
from project.database import create_all_tables
from project.database import AsyncSession, get_async_session
from project.models import Post

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield       

app = FastAPI(lifespan=lifespan)

@app.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate, session: AsyncSession = Depends(get_async_session)):
    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    return post

@app.get("/posts")
async def get_posts():
    pass