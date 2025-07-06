from fastapi import FastAPI
from pydantic import BaseModel
#pip install fastapi uvicorn
class User(BaseModel):
    user_id: int
    grade: float
    graduate: bool = None

test = FastAPI()
'''
To check documentation, go to the following endpoints
1. /redoc -> redoc: reading the documentation only
2. /docs -> SwaggerUI: can try out the api
'''

@test.get("/")
def read_root():
    return {"message": "Welcome to FastAPI updated!!!"}

#Let's write other endpoints

@test.get('/users/{user_id}')
def get_user(user_id: int, q: str=None):
    return {"user id": user_id, "query": q}

@test.post("/users/")
def create_user(user: User):
    return {"User ID": user.user_id, "Grade": user.grade, "Graduated": "Yes" if user.graduate else "No"}
    