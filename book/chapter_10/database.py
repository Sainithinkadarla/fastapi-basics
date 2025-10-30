from chapter_10.settings import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from collections.abc import AsyncGenerator

engine = create_async_engine(settings.db_url)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session 
