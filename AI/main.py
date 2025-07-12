from fastapi import FastAPI
from model import get_model
from pydantic import BaseModel

app = FastAPI()

class Text(BaseModel):
    text:str

model = get_model()

@app.post("/predict")
async def predict(txt: Text):
    result = model.predict(txt.text)
    return {"Text":txt, "Sentiment": result[0]["label"], "Confidence":  result[0]["score"]}