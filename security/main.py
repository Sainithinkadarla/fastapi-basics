from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

class Item(BaseModel):
    name:str
    description: str
    price: float
    tax: float = None

app = FastAPI()

@app.exception_handler(ValidationError)
async def Custom_Validation_Error_Handling(req: Request, e: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"message": "Custom Validation Error", 'detail': e.errors()}
        )

@app.post("/validate")
async def create_user(data:dict):
    user = User.validate(data)
    return {"message": "User is valid", "user": user}

@app.post("/items")
async def create_item(item: Item):
    return {"Name":item.name, "Description": item.description}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    items = [1,2]
    if item_id not in items:
        raise HTTPException(status_code=404, 
                            detail="Item Not found")
    
    return {"Item ID": items[items.index(item_id)]}