#!pip install passlib, python-dotenv, pyjwt, python-multipart
import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

load_dotenv()

KEY = os.getenv("SECRET")
ALGORITHM = "HS256"
EXPIRE_TIME = 30


oauthscheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def create_access_token(data:dict, expire_delta:timedelta=None):
    if expire_delta is None:
        expire_delta = timedelta(minutes=EXPIRE_TIME)

    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"expire":expire.isoformat()})
    encoded = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded

def create_access_token_role(data:dict, role:str, expire_delta:timedelta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta if expire_delta else expire_delta = timedelta(minutes=EXPIRE_TIME)
    to_encode.update({"expire":expire.isoformat(), "role": role})
    encoded = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded

def verify_token(token:str):
    try:
        decoded = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.PyJWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate":"Bearer"}
        )