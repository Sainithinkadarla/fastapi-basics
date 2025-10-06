from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def users_home():
    return {"message": "Users root endpoint"}