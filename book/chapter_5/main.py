from fastapi import FastAPI, Depends, Query, HTTPException, status, Header, APIRouter
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class Post(PostBase):
    id: int
    views: int = 0

class PostRead(PostBase):
    id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class DB():
    posts: dict[int, Post] = {}

db = DB()

def secret_header(secret_header: str | None = Header(None)) -> None:
    if not secret_header or secret_header != "secret-value":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
app = FastAPI(dependencies=[Depends(secret_header)])

# function dependency
async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)

@app.get("/items")
async def items_page(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

## resusing the function in another endpoint
@app.get("/things")
async def things_list(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

## dependency function with validation
async def valid_pagination(skip: int = Query(0, ge = 0), 
                           limit: int = Query(10, ge = 0)
                           ) -> tuple[int, int]:
    
    capped_limit = min(limit, 100)
    return (skip, capped_limit)

@app.get("/posts")
async def list_posts(p: tuple[int, int] = Depends(valid_pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}

## Get an object or raise a 404 error

async def get_post_obj(id: int):
    try:
        return db.posts[id]
    except:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

@app.get("/list-posts")
async def get_all_posts():
    return db.posts

@app.post("/posts", response_model= PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    new_id = int(max(db.posts.keys() or (0,))) + 1
    new_post = Post(id = new_id, **post.model_dump())

    db.posts[new_id] = new_post
    return new_post

@app.get("/posts/{id}")
async def get_post(post: Post = Depends(get_post_obj)):
    return post

@app.patch("/posts/{id}", response_model=PostRead)
async def update_post( update_post: PostUpdate, 
                      post: Post = Depends(get_post_obj)):
    update_fields = update_post.model_dump(exclude_unset = True)
    new_post = post.model_copy(update=update_fields)

    db.posts[post.id] = new_post
    return new_post

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(post: Post = Depends(get_post_obj)):
    db.posts.pop(post.id)
    # return None


# Parameterized dependency with class
class Pagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def __call__(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)

pagination = Pagination(maximum_limit=500)

@app.get("/pets")
async def list_pets(p: tuple[int, int] = Depends(pagination)):
    return {"skip": p[0], "limit": p[1]}

## Using class methods as dependencies
class CustomPagination:
    def __init__(self, maximum_limit):
        self.maximum_limit = maximum_limit

    async def skip_limit(self, skip: int = Query(0, ge=0), 
                         limit: int = Query(10, ge=0)
                         ) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)
    
    async def page_size(self, page: int = Query(1, ge=1),
                        size: int = Query(10, ge=0)
                        ) -> tuple[int, int]:
        capped_size = min(self.maximum_limit, size)
        return (page, capped_size)
    
custom_pagination = CustomPagination(maximum_limit = 50)

@app.get("/houses")
async def get_houses(p: tuple[int, int] = Depends(custom_pagination.skip_limit)):
    return {"skip": p[0], "limit": p[1]}

@app.get("/blogs")
async def get_blogs(p: tuple[int, int] = Depends(custom_pagination.page_size)):
    return {"page": p[0], "size": p[1]}


# Dependencies at path, router, global level
## path decorator level
# secret-header function is implmented at line 27
    
@app.get("/protected-route", dependencies=[Depends(secret_header)])
async def protect_route():
    return {"hello": "world"}

## router level decorator level
### setting at APIRouter object instantiation
student_router = APIRouter(dependencies=[Depends(secret_header)])

@student_router.get("/r1")
async def route1():
    return {"Message": "student Route 1"}

@student_router.get("/r2")
async def route2():
    return {"Message": "student Route 2"}

app.include_router(student_router, prefix="/students")

### setting in include_router method

teachers_router = APIRouter()

@teachers_router.get("/r1")
async def route1():
    return {"Message": "teachers Route 1"}

@teachers_router.get("/r2")
async def route2():
    return {"Message": "teachers Route 2"}

app.include_router(teachers_router, prefix="/teachers", dependencies=[Depends(secret_header)])


### global app level dependency
# I implemented for this app itself check at line 31