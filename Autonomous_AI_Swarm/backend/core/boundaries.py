from enum import Enum
from pydantic import BaseModel
from typing import List

class AgentRole(str, Enum):
    MANAGER = "Manager"
    RESEARCHER = "Researcher"
    QA = "QA"

class PermissionMatrix(BaseModel):
    allowed_actions: List[str]
    forbidden_actions: List[str]

BOUNDARIES = {
    AgentRole.MANAGER: PermissionMatrix(
        allowed_actions=["delegate_task", "summarize_results", "mark_completed", "mark_failed"],
        forbidden_actions=["execute_subtask", "review_subtask"]
    ),
    AgentRole.RESEARCHER: PermissionMatrix(
        allowed_actions=["search_web", "gather_data", "write_draft", "execute_subtask"],
        forbidden_actions=["delegate_task", "approve_subtask", "reject_subtask"]
    ),
    AgentRole.QA: PermissionMatrix(
        allowed_actions=["review_subtask", "approve_subtask", "reject_subtask", "provide_feedback"],
        forbidden_actions=["execute_subtask", "delegate_task", "search_web"]
    )
}
