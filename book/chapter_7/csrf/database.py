from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from models import Base
from collections.abc import AsyncGenerator

DB_URL = "sqlite+aiosqlite:///app.db"

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)