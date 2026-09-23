from fastapi import APIRouter, HTTPException
from typing import List, Dict
from models.workflow import Workflow, ExecutionResult
from services.workflow_engine import WorkflowEngine

router = APIRouter(prefix="/workflows", tags=["workflows"])

# In-memory store for demonstration
workflows_db: Dict[str, Workflow] = {}

@router.post("/", response_model=Workflow)
def create_workflow(workflow: Workflow):
    workflows_db[workflow.id] = workflow
    return workflow

@router.get("/", response_model=List[Workflow])
def list_workflows():
    return list(workflows_db.values())

@router.get("/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: str):
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflows_db[workflow_id]

@router.post("/{workflow_id}/execute", response_model=ExecutionResult)
def execute_workflow(workflow_id: str):
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    workflow = workflows_db[workflow_id]
    engine = WorkflowEngine(workflow)
    result = engine.execute()
    
    # Save state back
    workflows_db[workflow_id] = workflow
    
    return ExecutionResult(
        workflow_id=workflow_id,
        status=result["status"],
        node_results=result["node_results"]
    )
