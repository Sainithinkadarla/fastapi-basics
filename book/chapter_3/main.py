from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Cookie, Request, status, Response, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse
from enum import Enum
from pydantic import BaseModel

import pathlib

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

@app.get("/posts_res/{id}", response_model=PublicPost)
async def get_res_post(id: int):
    return posts[id]

# The Response parameter
# Import Response from the fastapi package
## Setting headers
@app.get("/customHeader")
async def get_custom_header(response: Response):
    response.headers["My-custom-Header"] = "My-Custom-Header-Value"
    return {"Message": "See the header"}

## Setting cookies
@app.get("/getcookie")
async def custom_header(response: Response):
    response.set_cookie("Mycookie", "Cookie-Value", max_age=86400)
    return {"Message": "See the header for cookie"}

## Setting the status code dynamically
@app.put("/posts/{id}")
async def create_post(id: int, post: Post, response: Response):
    if id not in posts:
        posts[id] = post
        response.status_code = status.HTTP_201_CREATED
    return posts[id]

@app.get("/posts")
async def get_all_posts():
    return posts

# Rasing HTTP Errors
# Import HTTPException class from fastapi package
@app.post("/passwd_check")
async def passwd_match(passwd: str = Body(...), confirm_passwd: str = Body(...)):
    if passwd != confirm_passwd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "Message": "Password doesn't match",
                "hints": ["Check caps lock on your keyboard", "Try to  make the password visible by clicking "]
            }
        )
    return {"Message": "Passwords match!"}

# Building Custom response
# Import HTMLResponse and PlainTextResponse from fastapi.responses
@app.get("/html", response_class= HTMLResponse)
async def get_html():
    return """
                <html>
                <head>
                    <title>Sample page</title>
                </head>
                    <body>
                        <h1>This a  heading 1</h1>
                        <p> This is a body</p>
                    </body>
                </html>
            """

@app.get("/text", response_class = PlainTextResponse)
async def get_plaintext():
    return "Hello this is a plain text"

## Redirection
# Import RedirectReponse from fastapi.responses
@app.get("/redirect")
async def redirect():
    return RedirectResponse("/posts")

## hanging the status code with RedirectResponse object
@app.get("/redirect_status")
async def another_redirect():
    return RedirectResponse("/posts", status_code=status.HTTP_301_MOVED_PERMANENTLY)

## FileResponse
# Import FileResponse from fastapi.responses
# import Path from pathlib
@app.get("/file")
async def get_file():
    root_dir = pathlib.Path(__file__).parent.parent
    response_file = root_dir / "sample.png"
    return FileResponse(response_file, filename = "test.png")

## Custom response
@app.get("/xml")
async def custom_response():
    content = """<?xml version="1.0" encoding="UTF-8"?>
        <Hello>World</Hello>
    """
    return Response(content= content, media_type="application/xml")