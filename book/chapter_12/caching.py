from contextlib import asynccontextmanager
import os
from pydantic import BaseModel
from sklearn.pipeline import Pipeline
from fastapi import FastAPI, Depends, status
import joblib

memory = joblib.Memory(location="cache.joblib")

@memory.cache(ignore=["model"])
def predict(model: Pipeline, text: str):
    prediction = model.predict([text])
    return prediction[0]

class PredictionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    category: str

class NewsGroupModel:
    model: Pipeline | None = None
    targets: list[str] | None = None

    def load_model(self):
        model_file = os.path.join(os.path.dirname(__file__), "model.joblib")
        loaded_model = joblib.load(model_file)

        model, targets = loaded_model
        self.model = model
        self.targets = targets
    
    async def predict(self, input: PredictionInput):
        if not self.model or not self.targets:
            raise RuntimeError("model is not loaded")
        prediction = predict(self.model, input.text)
        category = self.targets[prediction]
        return PredictionOutput(category=category)
    
news_group_model = NewsGroupModel()

@asynccontextmanager
async def lifespan(app:FastAPI):
    news_group_model.load_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def prediction(output: PredictionOutput = Depends(news_group_model.predict)):
    return output

@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
    memory.clear()