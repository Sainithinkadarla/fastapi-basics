import io
from fastapi import WebSocket, FastAPI, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import torch
from transformers import YolosForObjectDetection, YolosImageProcessor
from PIL import Image, ImageDraw
from pathlib import Path
from pydantic import BaseModel 
import asyncio

class Object(BaseModel):
    box: tuple[float, float, float, float ]
    label: str

class Objects(BaseModel):
    objects: list[Object]

class ObjectDetection:
    image_processor: YolosImageProcessor | None = None
    model: YolosForObjectDetection | None = None

    def load_model(self):
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        self.model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

    def predict(self, image: Image.Image):
        if not self.image_processor or not self.model:
            raise RuntimeError("Model not loaded")
        
        inputs = self.image_processor(images = image, return_tensors = "pt")
        outputs = self.model(**inputs)

        target_sizes = [image.size[::-1]]
        results = self.image_processor.post_process_object_detection(outputs=outputs, 
                                                                     threshold=0.7, 
                                                                     target_sizes=target_sizes)[0]
        
        objects: list[Object] = []
        for score, box, label in zip(results['scores'], results["boxes"], results["labels"]):
            if score > 0.7:
                box_values = box.tolist()
                label = self.model.config.id2label[label.item()]
                objects.append(Object(box = box_values, label=label))
                
        return Objects(objects=objects)

object_detection = ObjectDetection()

@asynccontextmanager
async def lifespan(app:FastAPI):
    object_detection.load_model()
    yield

app = FastAPI(lifespan=lifespan)

async def receive(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await websocket.receive_bytes()
        try:
            queue.put_nowait(bytes)
        except asyncio.QueueFull:
            pass

async def detect(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await queue.get()
        image = Image.open(io.BytesIO(bytes))
        objects = object_detection.predict(image)
        await websocket.send_json(objects.model_dump())

@app.websocket("/predict")
async def object_detection_prediction(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue(1)
    receive_task = asyncio.create_task(receive(websocket, queue))
    detect_task = asyncio.create_task(detect(websocket, queue))
    try:
        done, pending = await asyncio.wait((receive_task, detect_task),
                                        return_when=asyncio.FIRST_COMPLETED)
        for t in pending:
            t.cancel()
        for t in done:
            t.result()
    except WebSocketDisconnect:
        pass

@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "index.html")

staticfiles_app = StaticFiles(directory=Path(__file__).parent / "assets")
app.mount("/assets", staticfiles_app)