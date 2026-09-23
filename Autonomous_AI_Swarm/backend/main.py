from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers.task_router import router as task_router
from services.swarm_orchestrator import swarm_orchestrator
import asyncio

app = FastAPI(title="Autonomous AI Swarm")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    async def send_message(msg: str):
        try:
            await websocket.send_text(msg)
        except Exception:
            pass

    await swarm_orchestrator.register_connection(send_message)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
