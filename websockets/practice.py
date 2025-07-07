from fastapi import FastAPI, WebSocket

app = FastAPI()

active_connections = []

@app.websocket("/broadcast")
async def broadcast_all(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            for connection in active_connections:
                if connection != websocket:
                    await connection.send_text(f"Broadcast message: {msg}")
    except Exception as e:
        print(f"Error: {e}")
        active_connections.remove(websocket)
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        await websocket.close()
