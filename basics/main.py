from fastapi import FastAPI

test = FastAPI()

@test.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!!!"}