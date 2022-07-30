from fastapi import WebSocket, WebSocketDisconnect

from app.main import app
from app.websocket.manager import connection_manager


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(f"A message from client {client_id}: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
