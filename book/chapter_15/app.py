from fastapi import FastAPI, Depends, status, Header, HTTPException
from logger import logger

def secret_header(secret_header: str | None = Header(None)):
    logger.debug("Check secret header")
    if not secret_header or secret_header != "secret":
        logger.warning("Invalid or missing secret header")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
app = FastAPI(dependencies=[Depends(secret_header)])

@app.get("/r1")
def route1():
    return {"Message": "r1"}

@app.get("/r2")
def route2():
    return {"Message": "r2"}