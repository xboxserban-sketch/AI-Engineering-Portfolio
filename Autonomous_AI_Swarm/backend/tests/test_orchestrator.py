import pytest
from core.boundaries import BOUNDARIES, AgentRole
from services.agents.manager_agent import ManagerAgent
from models.agent import AgentModel, Message, MessageType
from services.swarm_orchestrator import SwarmOrchestrator

@pytest.mark.asyncio
async def test_agent_boundaries():
    assert "execute_subtask" not in BOUNDARIES[AgentRole.MANAGER].allowed_actions
    assert "review_subtask" not in BOUNDARIES[AgentRole.RESEARCHER].allowed_actions

@pytest.mark.asyncio
async def test_task_lifecycle():
    orch = SwarmOrchestrator()
    task = await orch.submit_task("Test task")
    assert task.status == "pending" or task.status == "in_progress"

@pytest.mark.asyncio
async def test_message_routing():
    agent = ManagerAgent(AgentModel(name="Test", role=AgentRole.MANAGER, permissions=BOUNDARIES[AgentRole.MANAGER]))
    msg = Message(id="1", from_agent="System", to_agent="Manager", content="Hi", message_type=MessageType.SYSTEM)
    response = await agent.process_message(msg, [])
    assert response.to_agent == "Researcher"

@pytest.mark.asyncio
async def test_websocket_message_format():
    msg = Message(id="1", from_agent="A", to_agent="B", content="Hello", message_type=MessageType.SYSTEM)
    assert "Hello" in msg.model_dump_json()

@pytest.mark.asyncio
async def test_rejection_flow_boundaries():
    assert "reject_subtask" in BOUNDARIES[AgentRole.QA].allowed_actions
