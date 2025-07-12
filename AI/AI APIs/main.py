from fastapi import FastAPI
from utils import generate_text


app = FastAPI()

@app.post("/generate")
async def generate_endpoint(prompt:str):
    response = generate_text(prompt)
    return {"Prompt": prompt, "Response": response}