import httpx
import pytest_asyncio
import pytest
import asyncio
from asgi_lifespan import LifespanManager
from ..chapter_6.mongodb_project.app import app, status
from ..chapter_6.mongodb_project.database import get_db, AsyncIOMotorClient
from ..chapter_6.mongodb_project.models import Post

client = AsyncIOMotorClient("mongodb://172.17.0.6:27017")
db_test = client["sample_test"]

def get_test_db():
    return db_test


@pytest.fixture(scope="session")
async def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        app.dependency_overrides[get_db] = get_test_db
        async with httpx.AsyncClient(base_url="http://localhost:8000") as test_client:
            yield test_client

@pytest_asyncio.fixture(autouse=True, scope="module")
async def create_dummy_db():
    initial_posts = [
        Post(title="title1", content="This is content"),
        Post(title="title2", content="This is content"),
        Post(title="title3", content="This is content"),
        Post(title="title4", content="This is content")
    ]

    await db_test["posts"].insert_many(
        [post.model_dump(by_alias = True) for post in initial_posts])
    
    yield initial_posts

    await client.drop_database("sample_test")

@pytest.mark.asyncio
class TestGetCases:
    async def test_non_existing(self, test_client):
        response = await test_client.get("/posts/sfds")

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    async def test_existing(self, test_client, create_dummy_db):
        response = await test_client.get(f"/posts/{create_dummy_db[0].id}")
        
        assert response.status_code == status.HTTP_200_OK