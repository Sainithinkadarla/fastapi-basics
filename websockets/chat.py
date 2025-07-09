from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager():
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[websocket] = username
        await self.broadcast(f"+ {username} joined the chat")

    async def broadcast(self, msg: str):
        disconnected_clients = []
        for connection in self.active_connections.keys():
            try:
                await connection.send_text(msg)
            except:
                disconnected_clients.append(connection)

        for connection in disconnected_clients:
            self.active_connections.pop(connection, None)
    
    async def disconnect_all(self):
        connections = list(self.active_connections.keys())
        for connection in connections:
            await connection.close()
            self.active_connections.pop(connection, None)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            username = self.active_connections.pop(websocket)
            await self.broadcast(f"- {username} has disconnected the chat!")
        
            if username.lower() == "admin":
                await self.broadcast("Admin has left the chat".upper())
                await self.disconnect_all()

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def chat_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            msg = await websocket.receive_text()
            await manager.broadcast(f"{username}: {msg}")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

