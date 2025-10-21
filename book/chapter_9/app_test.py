import pytest
import pytest_asyncio
import asyncio
from asgi_lifespan import LifespanManager
from app import app
from fastapi import status
import httpx

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture()
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(base_url="http://localhost:8000") as test_client:
                yield test_client

@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    print(json_response)
    assert json_response == {"Message": "Hello"}