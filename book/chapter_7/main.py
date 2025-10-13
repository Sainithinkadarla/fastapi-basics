from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import APIKeyHeader

api_token = "secret"

apikeyheader = APIKeyHeader(name="Token")

app = FastAPI()

@app.get("/protected")
async def protected_route(token: str = Depends(apikeyheader)):
    if token != api_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"Message": "Welcome"}


