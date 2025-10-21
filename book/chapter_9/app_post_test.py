from app_post import app, status
import pytest
import pytest_asyncio 
import httpx
from asgi_lifespan import LifespanManager
import asyncio


@pytest.fixture(scope="session")
async def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(base_url="http://localhost:8000") as test_client:
            yield test_client

@pytest.mark.asyncio
class TestPostPerson:
    async def test_invalid(self, test_client: httpx.AsyncClient):
        payload = {"name" : "kim"}
        response = await test_client.post("/people", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    
    async def test_valid(self, test_client: httpx.AsyncClient):
        payload = {"name" : "kim", "age": 21}
        response = await test_client.post("/people", json=payload)

        assert response.status_code == status.HTTP_201_CREATED

        assert response.json() == payload

