import time
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/async")
async def async_task():
    start = time.perf_counter()
    await asyncio.sleep(5)
    end = time.perf_counter()
    print(f"{end-start:.2f} seconds")
    return {"Message": "This is asynchronous task"}

@app.get("/sync")
def sync_task():
    time.sleep(5)
    return {"Message": "This is synchronous task"}