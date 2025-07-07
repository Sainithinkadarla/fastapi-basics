import asyncio
from fastapi import FastAPI, BackgroundTasks


async def lifespan(app):
    print("Server is starting")
    yield
    print("Server is closing")

app = FastAPI(lifespan=lifespan)

async def lengthy_task():
    for i in range(5):
        await asyncio.sleep(1)
        with open("log.txt", 'a') as f:
            f.write(f"Job {i}\n")

@app.post("/bgtask")
async def bgtask(bg: BackgroundTasks):
    bg.add_task(lengthy_task)
    return {"Message": "Task is scheduled"}