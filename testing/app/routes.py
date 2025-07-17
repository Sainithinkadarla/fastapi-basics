from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Item

router = APIRouter()

@router.post("/items/")
def create_item(name:str, description: str, db: Session = Depends(get_db)):
    item = Item(name=name, description= description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/items/{item_id}")
def get_item(item_id: int, db:Session= Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail= "Item not found")
    return item 