from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Counter
from fastapi import FastAPI
from random import randint

app = FastAPI()

DICE_COUNTER = Counter("app_dice_rolls_total_drama", 
                       "Total number of dice rolls per face", 
                       labelnames=["face"])

@app.get("/dice")
async def dice_rolls():
    face = randint(1, 6)
    DICE_COUNTER.labels(face).inc()
    return {"Result": face}

instrumentator = Instrumentator()
instrumentator.add(metrics.default())
instrumentator.instrument(app).expose(app)