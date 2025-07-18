from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, String, Integer

Base = declarative_base()
app = FastAPI()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, autoincrement=True, index= True, primary_key=True)
    name = Column(String, index = True)
    description = Column(String, index = True)

database_url = "postgresql://fastapi_user:chanduk1234@40.90.236.51/fastapi_db"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)
 
Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items")
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    item = Item(name=name, description = description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "description": item.description}

@app.get("/items/{item_id}")
async def get_item(item_id: int, db: Session=Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail= "Item not found")
    return {"id": item.id, "name": item.name, "description": item.description}
    # return item
