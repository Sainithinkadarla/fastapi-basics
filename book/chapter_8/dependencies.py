from fastapi import FastAPI, status, Depends, WebSocket, Cookie, WebSocketException
from starlette.websockets import WebSocketDisconnect

api_token = "SECRET_API_TOKEN"

app = FastAPI()

@app.websocket("/ws")
async def socket(websocket: WebSocket, username: str = "Anoynmous", token: str = Cookie(...)):
    if api_token != token:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()

    await websocket.send_text(f"Welcome {username}")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message recieved : {data}")
    except WebSocketDisconnect:
        pass