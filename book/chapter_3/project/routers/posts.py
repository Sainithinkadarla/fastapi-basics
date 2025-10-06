from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def posts_home():
    return {"message": "posts root endpoint"}