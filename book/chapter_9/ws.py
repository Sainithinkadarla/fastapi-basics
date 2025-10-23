from fastapi import WebSocket, FastAPI
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def web_socket_communication(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message recieved : {data}")
    except WebSocketDisconnect:
        pass