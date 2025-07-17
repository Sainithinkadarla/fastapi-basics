from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routes import router
from external_api import external_data

app = FastAPI(title="API testing")

app.include_router(router)

@app.get("/")
def home():
    return {"Message": "Welcome to api"}

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept()
    active_connections.append(websocket)
    try: 
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"Message received: {message}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.get("/external-data")
async def fetch_external():
    return await external_data()