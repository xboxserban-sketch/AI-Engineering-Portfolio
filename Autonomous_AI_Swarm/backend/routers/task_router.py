from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.swarm_orchestrator import swarm_orchestrator
from models.agent import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskRequest(BaseModel):
    description: str

@router.post("/", response_model=Task)
async def submit_task(req: TaskRequest):
    return await swarm_orchestrator.submit_task(req.description)

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    task = swarm_orchestrator.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
