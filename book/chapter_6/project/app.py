from fastapi import FastAPI, status, HTTPException, Depends, Query
from contextlib import asynccontextmanager
from sqlalchemy import select

from project.schemas import PostCreate, PostPartialUpdate, PostRead
from project.database import create_all_tables
from project.database import AsyncSession, get_async_session
from project.models import Post

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield       

async def pagination(skip: int = Query(0, ge=0), 
                     limit: int = Query(10, ge=10)):
    capped_limit = min(100, limit)
    return (skip, capped_limit)

async def get_post_or_404(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.id == id)
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return post


app = FastAPI(lifespan=lifespan)

# creating a object
@app.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate, session: AsyncSession = Depends(get_async_session)):
    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    return post

# getting all objects
@app.get("/posts", response_model=list[PostRead])
async def get_posts(pagination: tuple[int, int] = Depends(pagination), 
                    session: AsyncSession = Depends(get_async_session)):
    skip, limit = pagination
    #Import select function from sqlalchemy package
    query = select(Post).offset(skip).limit(limit)
    results = await session.execute(query)
    return results.scalars().all()

# getting single object
@app.get("/posts/{id}", response_model=PostRead)
async def get_post(post: Post = Depends(get_post_or_404)):
    return post

# updating objects