import os 
import joblib
from sklearn.pipeline import Pipeline
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel

class PredictionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    category: str

class NewsGroupModel:
    model: Pipeline | None = None 
    targets: list[str]

    def load_model(self):
        model_file = os.path.join(os.path.dirname(__file__), "model.joblib")
        loaded_model = joblib.load(model_file)

        model, targets = loaded_model

        self.model = model
        self.targets = targets
    
    async def predict(self, input: PredictionInput):
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        
        prediction = self.model.predict([input.text])
        category = self.targets[prediction[0]]
        return PredictionOutput(category=category)
    
newsgroup_model = NewsGroupModel()

@asynccontextmanager
async def lifespan(app:FastAPI):
    newsgroup_model.load_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def prediction(output: PredictionOutput = Depends(newsgroup_model.predict)):
    return output