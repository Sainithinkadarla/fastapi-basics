from fastapi import FastAPI, WebSocket, status, WebSocketException
import broadcaster
import asyncio
from pydantic import BaseModel
from contextlib import asynccontextmanager
from starlette.websockets import WebSocketDisconnect

@asynccontextmanager
async def lifespan(websocket:WebSocket):
    await broadcast.connect()
    yield 
    await broadcast.disconnect()

broadcast = broadcaster.Broadcast("redis://172.17.0.3:6379")
channel = "chat"

class MessageEvent(BaseModel):
    username: str 
    message: str



async def receive_message(websocket: WebSocket, username: str):
    async with broadcast.subscribe(channel=channel) as subscriber:
        async for event in subscriber:
            message_event = MessageEvent.model_validate_json(event.message)
            if message_event.username != username:
                await websocket.send_json(message_event.model_dump())

async def send_message(websocket: WebSocket, username: str):
    data = await websocket.receive_text()
    event = MessageEvent(username=username, message=data)
    await broadcast.publish(channel, message=event.model_dump_json())

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def endpoint(username: str, websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            receive_task = asyncio.create_task(receive_message(websocket=websocket,username=username))
            send_task = asyncio.create_task(send_message(websocket=websocket,username=username))
            done, pending = await asyncio.wait({receive_task, send_task},
                                               return_when=asyncio.FIRST_COMPLETED)
            for t in pending:
                t.cancel()
            for t in done:
                t.result()
    except WebSocketDisconnect:
        pass