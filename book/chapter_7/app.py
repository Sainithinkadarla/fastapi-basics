from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

apikeytoken = "secret"
apikeyheader = APIKeyHeader(name='Token')

app = FastAPI()


async def authenticate(token: str = Depends(apikeyheader)):
    if token != apikeytoken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
@app.get("/protected", dependencies=[Depends(authenticate)])
async def protected_message():
    return {"Message": "Welcome"}