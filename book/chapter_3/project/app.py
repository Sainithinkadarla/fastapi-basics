from fastapi import FastAPI
from project.routers.users import router as users_router
from project.routers.posts import router as posts_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags= ["users_tag"])
app.include_router(posts_router, prefix = "/posts", tags = ["posts_tag", "tag2_posts"])