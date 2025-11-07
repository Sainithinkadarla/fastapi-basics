from fastapi import FastAPI, status, Depends
from contextlib import asynccontextmanager 
from database import create_all_tables, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import GeneratedImageCreate, GeneratedImageRead
from models import GenereatedImages
from worker import text_to_image_task

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_all_tables()
    yield  

app = FastAPI(lifespan=lifespan)

@app.post("/generated-images", 
          status_code=status.HTTP_201_CREATED,
          response_model=GeneratedImageRead)
async def create_generated_image(generate_image_create: GeneratedImageCreate,
                                 session: AsyncSession = Depends(get_db)):
    image = GenereatedImages(**generate_image_create.model_dump())
    session.add(image)
    await session.commit()

    text_to_image_task(id=image.id)

    return image