import pytest
from asgi_lifespan import LifespanManager
from httpx_ws.transport import ASGIWebSocketTransport
from httpx_ws import aconnect_ws
import httpx
from book.chapter_9.ws import app


@pytest.mark.asyncio
async def test_ws():
    async with LifespanManager(app):
        transport = ASGIWebSocketTransport(app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="ws://testserver"
        ) as client:

            async with aconnect_ws("/ws", client=client) as websocket:
                text = "Hello"
                await websocket.send_text(text)

                message = await websocket.receive_text()
                assert message == f"Message recieved : {text}"
