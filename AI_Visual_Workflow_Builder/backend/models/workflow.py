from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class NodeType(str, Enum):
    LLM_ANALYZE = "LLM_ANALYZE"
    FILTER = "FILTER"
    TRANSFORM = "TRANSFORM"
    NOTIFY = "NOTIFY"

class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class NodeConfig(BaseModel):
    prompt: Optional[str] = None
    regex: Optional[str] = None
    mapping: Optional[Dict[str, str]] = None
    target: Optional[str] = None

class Node(BaseModel):
    id: str
    type: NodeType
    config: NodeConfig = Field(default_factory=NodeConfig)
    status: ExecutionStatus = ExecutionStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Workflow(BaseModel):
    id: str
    name: str
    nodes: List[Node]
    edges: List[Edge]

class ExecutionResult(BaseModel):
    workflow_id: str
    status: ExecutionStatus
    node_results: Dict[str, Any]
