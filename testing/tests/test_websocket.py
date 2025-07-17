import pytest
from fastapi.testclient import TestClient
from app.main import app

testclient = TestClient(app)

@pytest.mark.asyncio
async def test_websocket():
    with testclient.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello world!")
        response = websocket.receive_text()
        print(response)
        assert "Message received: Hello world!" in response