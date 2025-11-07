from pydantic import BaseModel, Field
from datetime import datetime

class GeneratedImageBase(BaseModel):
    prompt: str
    negative_prompt: str | None = None
    steps: int = Field(50, ge=0, le=50)

    class Config:
        orm_mode = True

class GeneratedImageCreate(GeneratedImageBase):
    pass

class GeneratedImageRead(GeneratedImageBase):
    id: int
    created_at: datetime
    progress: int
    filename: str | None = None

class GeneratedImageURL(BaseModel):
    url: str