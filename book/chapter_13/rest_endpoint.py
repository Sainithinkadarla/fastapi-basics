from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, UploadFile, File
from transformers import YolosForObjectDetection, YolosImageProcessor
import torch  
from PIL import Image, ImageDraw
from pathlib import Path
from pydantic import BaseModel

class Object(BaseModel):
    box: tuple[float, float, float, float]
    label: str

class Objects(BaseModel):
    objects: list[Object]

class ObjectDetection():
    model: YolosForObjectDetection | None = None
    image_processor: YolosImageProcessor | None = None

    def load_model(self):
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        self.model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

    def predict(self, image: Image.Image) -> Objects:
        if not self.model or not self.image_processor:
            raise RuntimeError("Model is not loaded")
        
        inputs = self.image_processor(images=image, return_tensors = "pt")
        outputs = self.model(**inputs)

        target_sizes = [image.size[::-1]]
        results = self.image_processor.post_process_object_detection(
            outputs=outputs, threshold= 0.7, target_sizes=target_sizes
        )[0]

        objects: list[Object] = []

        for score, box, label in zip(results["scores"], results["boxes"], results["labels"]):
            if score > 0.7:
                box_values = box.tolist()
                label = self.model.config.id2label[label.item()]
                objects.append(Object(box=box_values, label=label))

        return Objects(objects=objects)

object_detection = ObjectDetection()

@asynccontextmanager
async def lifespan(app:FastAPI):
    object_detection.load_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict", response_model = Objects)
async def object_dection_func(image: UploadFile = File(...)):
    image_object = Image.open(image.file)
    return object_detection.predict(image=image_object)
