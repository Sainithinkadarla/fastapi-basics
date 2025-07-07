from fastapi import FastAPI
import httpx, time, requests
# !pip install httpx

app = FastAPI()

@app.get("/sync")
def sync_test():
    start = time.perf_counter()
    for i in range(5):
       requests.get(f"https://api.restful-api.dev/objects/{i}")
    end = time.perf_counter()
    execution_time = end - start
    return {"message": "Sync Function", "execution_time": execution_time}

@app.get("/async")
async def async_test():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        for i in range(5):
            await client.get(f"https://api.restful-api.dev/objects/{i}")
    end = time.perf_counter()
    execution_time = end - start
    return {"message": "Async Function", "execution_time": execution_time}