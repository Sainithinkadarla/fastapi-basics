from fastapi import FastAPI, Depends, status, HTTPException
from database import get_db, AsyncIOMotorDatabase
from bson import ObjectId, errors

from models import *

app = FastAPI()

async def get_post_or_404(id: str,
                           database: AsyncIOMotorDatabase = Depends(get_db)):
    raw_post = await database["posts"].find_one({"_id": id})

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Post(**raw_post)


@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate, database: AsyncIOMotorDatabase = Depends(get_db)):
    post = Post(**post_create.model_dump())

    upload_post = await database["posts"].insert_one(post.model_dump())
    # print(upload_post.inserted_id)
    result_post = await get_post_or_404(upload_post.inserted_id, database)
    return result_post