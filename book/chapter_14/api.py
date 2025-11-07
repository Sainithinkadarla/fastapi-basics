from dramatiq import Message
from worker import text_to_image_task
from fastapi import FastAPI, status
from pydantic import BaseModel, UUID4, Field

class ImageGenerationInput(BaseModel):
    prompt: str
    negative_prompt: str | None = None
    steps: int = Field(50, ge=1, le=50)

class ImageGenerationOutput(BaseModel):
    task_id: UUID4

app = FastAPI()

@app.post("/generate", status_code=status.HTTP_202_ACCEPTED,
           response_model=ImageGenerationOutput)
async def generate_image(input: ImageGenerationInput):
    task: Message = text_to_image_task.send(prompt=input.prompt, 
                                       negative_prompt=input.negative_prompt,
                                       steps=input.steps)
    print(task.message_id)
    return ImageGenerationOutput(task_id=task.message_id)