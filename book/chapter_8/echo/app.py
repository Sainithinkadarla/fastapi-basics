from fastapi import WebSocket, FastAPI
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def communicate(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message recieved : {data}")
        except WebSocketDisconnect:
            pass
