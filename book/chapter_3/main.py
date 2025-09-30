from fastapi import FastAPI, Path
from enum import Enum

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
