from fastapi import FastAPI, HTTPException, status, Depends
from security import create_access_token_role, verify_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
#!pip install passlib, python-dotenv, pyjwt, python-multipart

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

@app.post("/token")
async def login(formdata: OAuth2PasswordRequestForm = Depends()):
    user = User(username=formdata.username, password=formdata.password)

    if user.username == "admin" and user.password == "pass":
        # access_token = create_access_token({"sub":user.username})
        access_token = create_access_token_role({"sub":user.username}, role = "admin")
        return {"access_token": access_token, "token_type": "Bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authentication": "Bearer"}
    )

@app.get("/protected")
async def protected(token: str = Depends(verify_token)):
    return {"Message": "This is protected endpoint"}