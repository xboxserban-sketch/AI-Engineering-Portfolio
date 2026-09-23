from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from core.boundaries import AgentRole, PermissionMatrix

class MessageType(str, Enum):
    TASK_UPDATE = "task_update"
    AGENT_MESSAGE = "agent_message"
    SYSTEM = "system"
    ERROR = "error"

class Message(BaseModel):
    id: str
    from_agent: str
    to_agent: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: MessageType

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    conversation_log: List[Message] = []

class AgentModel(BaseModel):
    name: str
    role: AgentRole
    permissions: PermissionMatrix
