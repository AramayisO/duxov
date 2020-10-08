import io

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = open('kareri_amrots.opus', 'rb')
    await websocket.send_bytes(data.read())
