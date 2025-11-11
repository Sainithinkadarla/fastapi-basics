from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics

app = FastAPI()

@app.get("/")
async def home():
    return {"Message": "Hello world"}

instrumentator = Instrumentator()
instrumentator.add(metrics.default())
instrumentator.instrument(app).expose(app)