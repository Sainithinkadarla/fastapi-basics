from fastapi import FastAPI, status, Depends, HTTPException
from contextlib import asynccontextmanager 
from database import create_all_tables, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import GeneratedImageCreate, GeneratedImageRead, GeneratedImageURL
from models import GenereatedImages
from worker import text_to_image_task
from storage import Storage
from settings import settings

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield  

app = FastAPI(lifespan=lifespan)

async def get_storage():
    return Storage()

async def get_image_or_404(id: int, 
                           session: AsyncSession = Depends(get_db)):
    query = select(GenereatedImages).where(GenereatedImages.id == id)
    result = await session.execute(query)
    image = result.scalar_one_or_none()
    
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return image

@app.post("/generated-images", 
          status_code=status.HTTP_201_CREATED,
          response_model=GeneratedImageRead)
async def create_generated_image(generate_image_create: GeneratedImageCreate,
                                 session: AsyncSession = Depends(get_db)):
    image = GenereatedImages(**generate_image_create.model_dump())
    session.add(image)
    await session.commit()

    text_to_image_task.send(image.id)

    return image

@app.get("/generated-images/{id}")
async def get_progress(image: GenereatedImages = Depends(get_image_or_404)):
    return image

@app.post("/generated-images/{id}/url")
async def get_presigned_image_url(image: GenereatedImages = Depends(get_image_or_404),
                                  storage: Storage = Depends(get_storage)):
    if image.filename is None: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="There is no such image. Please try again")
    url = storage.get_presigned_url(object_name=image.filename, bucket_name=settings.storage_bucket)

    return GeneratedImageURL(url=url)
