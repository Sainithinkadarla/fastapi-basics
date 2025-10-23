from book.chapter_9.ext_api import app, external
from fastapi import status
import pytest
from asgi_lifespan import LifespanManager
import pytest_asyncio
import asyncio
import httpx
print(app)

class MockExternalAPI:
    mock_data = {
        "products": [
            {
                "id": 1,
                "title": "iPhone 9",
                "description": "An apple mobile which is nothing like apple",
                "thumbnail": "https://i.dummyjson.com/data/products/1/thumbnail.jpg",
            }
        ],
        "total": 1,
        "skip": 0,
        "limit": 30,
    }
    async def __call__(self):
        return MockExternalAPI.mock_data

mock_external_api_instance = MockExternalAPI()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[external] = mock_external_api_instance
    async with LifespanManager(app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)
                                     , base_url="http://localhost:8000") as client:
            yield client

@pytest.mark.asyncio
async def test_ext(test_client: httpx.AsyncClient):
    response = await test_client.get("/products")

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json == MockExternalAPI.mock_data
