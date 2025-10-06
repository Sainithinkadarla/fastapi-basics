from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Cookie, Request, status, Response
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

# Form data and file uploads
## Form data
# Import Form function from fastapi
@app.post("/users-form")
async def form_data(name: str = Form(...), age: int = Form(...)):
    return {"Name" : name, "Age" : age}

## File upload
# import File function from fastapi
@app.post("/files")
async def upload_file(file: bytes = File(...)):
    return {"Length" : len(file)}

# File function is not efficient for larger file
# So, we have a class UploadFile
# import UploadFile function from fastapi
@app.post("/fileupload")
async def upload_file(file: UploadFile = File(...)):
    return {"Length" : file.size, "Type" : file.content_type, "Filename" : file.filename, "Extension" : file.filename.split('.')[1]}

@app.post("/multifile")
async def multi_file_upload(files : list[UploadFile] = File(...)):
    return { file.filename : {"Filename" : file.filename, 
                              "File Extension" : file.filename.split('.')[1], 
                              "File Length" : file.size } for file in files}


# Headers and cookies
## Headers
# Import Headers function from fastapi
@app.post("/")
async def headers(hello: str = Header(...)):
    return {"hello" : hello}

@app.get("/default-header")
async def get_default_header(user_agent: str = Header(...), accept_encoding: str = Header(...)):
    return {"user_agent" : user_agent, "length" : accept_encoding}

@app.get("/cookie")
async def get_cookie(hello : str | None = Cookie(None)):
    return {"cookie" : hello}

# Request object
# Import Request class from fastapi package
@app.get("/request")
async def get_req_obj(req: Request):
    return {"Message" : req.url}


# Response customization

# status code
# Inorder to change the status code, import status class/enum from fastapi
class Post(BaseModel):
    title: str

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

## When we have nothing to return like deleting a object

posts = {
    1: Post(title="My post", nb_views=100),
}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    posts.pop(id, None)
    return None

# The Response model
class ResPost(BaseModel):
    title: str
    nb_views: int

class PublicPost(BaseModel):
    title: str

@app.get("/posts/{id}", response_model=PublicPost)
async def get_res_post(id: int):
    return posts[id]

# The Response parameter
# Import Response from the fastapi package
## setting headers
@app.get("/customHeader")
async def get_custom_header(response: Response):
    response.headers["My-custom-Header"] = "My-Custom-Header-Value"
    return {"Message": "See the header"}