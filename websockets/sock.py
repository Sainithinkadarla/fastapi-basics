# !pip install uvicorn[standard]
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def end_point(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hi clientuuu!!!")
    await websocket.receive_text()
    await websocket.close()


@app.websocket("/chat")
async def chat_endpoint(websock: WebSocket):
    await websock.accept()

    while True:
        msg = await websock.receive_text()
        await websock.send_text(f"Received {msg}")
