from fastapi import FastAPI, status, HTTPException, Depends, Query
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas import PostCreate, PostPartialUpdate, PostRead, CommentRead, CommentCreate
from database import create_all_tables
from database import AsyncSession, get_async_session
from models import Post, Comment

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield       

async def pagination(skip: int = Query(0, ge=0), 
                     limit: int = Query(10, ge=10)):
    capped_limit = min(100, limit)
    return (skip, capped_limit)

async def get_post_or_404(id: int, session: AsyncSession = Depends(get_async_session)):
    query = (select(Post).options(selectinload(Post.comments)).where(Post.id == id))
    result = await session.execute(query)
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return post


app = FastAPI(lifespan=lifespan)

# creating a object
@app.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate, session: AsyncSession = Depends(get_async_session)):
    post = Post(**post_create.model_dump(), comments = [])
    session.add(post)
    await session.commit()
    return post

# getting all objects
@app.get("/posts", response_model=list[PostRead])
async def get_posts(pagination: tuple[int, int] = Depends(pagination), 
                    session: AsyncSession = Depends(get_async_session)):
    skip, limit = pagination
    #Import select function from sqlalchemy package
    query = select(Post).options(selectinload(Post.comments)).offset(skip).limit(limit)
    results = await session.execute(query)
    return results.scalars().all()

# getting single object
@app.get("/posts/{id}", response_model=PostRead)
async def get_post(post: Post = Depends(get_post_or_404)):
    return post

# updating objects
@app.patch("/posts/{id}", response_model=PostRead)
async def update_post(post_update: PostPartialUpdate, 
                      post: Post = Depends(get_post_or_404),
                      session: AsyncSession = Depends(get_async_session)):

    update_fields = post_update.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(post, key, value)

    session.add(post)
    await session.commit()

    return post

# deleting objects
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: Post = Depends(get_post_or_404), session: AsyncSession = Depends(get_async_session)):
    await session.delete(post)
    await session.commit()

@app.post("/posts/{id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, 
                         post : Post = Depends(get_post_or_404), 
                         session: AsyncSession = Depends(get_async_session)) -> Comment:
    comment = Comment(**comment.model_dump(), post = post)
    session.add(comment)
    await session.commit()
    
    return comment