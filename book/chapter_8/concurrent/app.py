from fastapi import FastAPI, WebSocket
import asyncio
from datetime import datetime
from starlette.websockets import WebSocketDisconnect

async def echo_message(websocket: WebSocket):
    data = await websocket.receive_text()
    await websocket.send_text(f"Message recieved : {data}")

async def date_time(websocket: WebSocket):
    await asyncio.sleep(10)
    await websocket.send_text(f"Current time : {datetime.now().isoformat()}")

app = FastAPI()

@app.websocket("/ws")
async def connection(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            echo_message_task = asyncio.create_task(echo_message(websocket))
            time_task = asyncio.create_task(date_time(websocket))
            done, pending = await asyncio.wait(
                {echo_message_task, time_task}, 
                return_when=asyncio.FIRST_COMPLETED)
            for t in pending:
                t.cancel()
            for t in done:
                t.result()
            
    except WebSocketDisconnect:
        pass
