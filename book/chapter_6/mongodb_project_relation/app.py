from fastapi import FastAPI, Depends, status, HTTPException, Query
from database import get_db, AsyncIOMotorDatabase
from bson import ObjectId, errors

from models import *

app = FastAPI()

async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def get_post_or_404(id: ObjectId = Depends(get_object_id),
                           database: AsyncIOMotorDatabase = Depends(get_db)):
    
    raw_post = await database["posts"].find_one({"_id": id})
    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return Post(**raw_post)

async def pagination(skip: int = Query(0, ge=0),
                     limit: int = Query(10, ge=0)
                    ):
    capped_limit = min(15, limit)
    return (skip, capped_limit)


@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_create: PostCreate,
                      database: AsyncIOMotorDatabase = Depends(get_db)):
    post = Post(**post_create.model_dump())

    upload_post = await database["posts"].insert_one(post.model_dump())
    print(upload_post.inserted_id, type(upload_post.inserted_id))
    result_post = await get_post_or_404(upload_post.inserted_id, database)
    return result_post

# Getting all documents
@app.get("/posts", response_model=list[Post])
async def get_all(database: AsyncIOMotorDatabase = Depends(get_db),                   
                      pagination: tuple[int, int] = Depends(pagination)):
    skip, limit = pagination
    query = database['posts'].find({}, skip = skip, limit = limit)
    results = [Post(**raw_post) async for raw_post in query]
    return results

# Getting a single object
@app.get("/posts/{id}", response_model=Post)
async def get_post(post: Post = Depends(get_post_or_404)):
    return post

# Updating the document
@app.patch("/posts/{id}")
async def update_post(post_update: PostPartialUpdate,
                      post: Post = Depends(get_post_or_404),
                      database: AsyncIOMotorDatabase = Depends(get_db)):
    
    update_fields = post_update.model_dump(exclude_unset=True)
    
    await database["posts"].update_one({"_id": post.id}, {"$set": update_fields})

    post = await get_post_or_404(post.id, database)
    return post

# Deleting the document
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(post: Post = Depends(get_post_or_404),
                      database: AsyncIOMotorDatabase = Depends(get_db)):
    await database["posts"].delete_one({"_id": post.id})


# Creating comment
@app.post("/posts/{id}/comments", response_model=list[Comment],
          status_code=status.HTTP_201_CREATED)
async def create_comment(comment_create: CommentCreate, 
                         database: AsyncIOMotorDatabase = Depends(get_db),
                         post: Post = Depends(get_post_or_404)):
    await database['posts'].update_one({"_id": post.id}, 
                                       {"$push":{"comments": comment_create.model_dump()} })
    updated_post = await get_post_or_404(post.id, database)

    return updated_post.comments
