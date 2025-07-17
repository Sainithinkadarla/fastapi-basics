from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# pip install pytest pytest-mock pytest-asyncio httpx sqlalchemy

engine = create_engine("sqlite:///../test.db")
SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()