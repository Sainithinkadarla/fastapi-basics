from ext_api import app
import pytest
from asgi_lifespan import LifespanManager
import pytest_asyncio
import asyncio
import httpx

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
    def __call__(self):
        return MockExternalAPI.mock_data

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_client():
    app.dependencies_overrides[external] = MockExternalAPI()
    async with LifespanManager():
        async with httpx.AsyncC