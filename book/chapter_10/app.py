from settings import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager 

@asynccontextmanager
async def lifespan(app:FastAPI):
    print(settings)
    yield
    print("Shutting down")

app = FastAPI(lifespan=lifespan)