from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
def lifespan(app: FastAPI):
    print("startup")
    yield
    print("shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Message": "Hello"}