from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
import random

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/stream/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await manager.connect(websocket)
    try:
        while True:
            # Simulate real-time data push
            data = {
                "symbol": symbol,
                "price": 150.0 + random.uniform(-1, 1),
                "timestamp": str(pd.Timestamp.now())
            }
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(1) # 1 sec update
    except WebSocketDisconnect:
        manager.disconnect(websocket)
