from fastapi import FastAPI, Path, Query, Body
from enum import Enum
from pydantic import BaseModel

class UserType(str, Enum):
    HR = 'hr'
    STANDARD = "standard"
    ADMIN = "admin"

app = FastAPI()

@app.get("/")
async def home():
    return {'Message': "Welcome Home"}

# Path parameters
@app.get("/users/{id}")
async def get_user_id(id: int):
    return {"Response": f"{id} is retrieved" }

@app.get("/users/{id}/{type}")
async def get_user_type_id(id: int, type: str):
    return {"id": id,
            "type": type }

@app.get("/users-enum/{id}/{type}")
async def get_user_type_id_with_enum(id: int, type: UserType):
    return {"id": id,
            "type": type }

@app.get("/users-path/{id}")
async def get_user_type_id_with_path(id: int = Path(..., le=1)):
    return {"id": id}

@app.get("/license-plates/{license}")
async def get_license(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}

@app.get("/license-plates-regex/{license}", description="It's a endpoint which uses regular expressions also")
async def get_license(license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license": license, "Result" : "Valid"}


# Query parameters
@app.get("/users")
async def get_user(page: int = 1, size: int = 10):
    return {"page" : page, "size" : size}

## required query parameter

class UsersType(str, Enum):
    BEST = "best"
    AVERAGE = "average"

@app.get("/type")
async def get_type(type: UsersType):
    return {"type" : type}

## Other validation options
# Import Query function from fastapi package
@app.get("/users_ad")
async def get_users(page: int = Query(1, ge=0), size: int = Query(10, le=100)):
    return {"page" : page, "size" : size}

# request body
# Import Body function from fastapi package
@app.post("/users_body")
async def  get_user_body(name: str = Body(...), age: int = Body()):
    return {"Name" : name, "Age" : age}

## Pydantic models
# import BaseModel class from Pydantic package
class User(BaseModel):
    name: str
    age: int

@app.post("/user-pyd")
async def get_user_post(user: User):
    return {"Name" : user.name, "Age" : user.age}


## Multiple objects
class Company(BaseModel):
    c_name: str
    c_location: str

@app.post("/users/create")
async def create_user(user: User, company: Company):
    return {"user" : user, "company" : company}

@app.post("/task")
async def create_task(user: User, priority: int = Body(..., ge=1, le=3)):
    return {"user" : user, "priority" : priority}
