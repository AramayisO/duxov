from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.music.service import MusicService

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connectins: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connectins.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connectins.remove(websocket)

    async def send(self, data: bytes, websocket: WebSocket):
        await websocket.send_bytes(data)

    async def broadcast(self, data: bytes):
        for connection in self.active_connectins:
            await connection.send_bytes(data)


manager = ConnectionManager()


@router.websocket("/ws")
async def music(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            request = await websocket.receive_json()
            
            try:
                seq = request["seq"]
            except KeyError:
                seq = 0
            
            packet = MusicService.get_next_audio_packet(seq=seq)
            meta = packet.dict()
            meta.pop("buffer")

            await websocket.send_json(meta)
            await websocket.send_bytes(packet.buffer)
            

    except WebSocketDisconnect:
        manager.disconnect(websocket)
