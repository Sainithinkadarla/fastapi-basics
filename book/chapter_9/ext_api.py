from typing import Any
from fastapi import FastAPI, Depends
import httpx

app = FastAPI()

class ExternalAPI:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url= "https://dummyjson.com")
    
    async def __call__(self) -> dict[str, Any]:
        async with self.client as client:
            response = await client.get("/products")
            return response.json()

external = ExternalAPI()

@app.get("/products")
async def get_products(products: dict[str, Any] = Depends(external)):
    return products