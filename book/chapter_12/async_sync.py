import time
from fastapi import FastAPI
import asyncio


app = FastAPI()

@app.get("/fast")
def fasting():
    return {"Message": "Fast"}

@app.get("/slow-async")
async def fasting():
    time.sleep(10)
    return {"Message": "Fast"}

@app.get("/slow-sync")
def fasting():
    time.sleep(10)
    return {"Message": "Fast"}

@app.get("/slow-fast-async")
async def fasting():
    await asyncio.sleep(10)
    return {"Message": "Fast"}
