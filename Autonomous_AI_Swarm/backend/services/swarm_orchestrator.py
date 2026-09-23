import asyncio
import uuid
from typing import Dict, List, Callable
from models.agent import Task, TaskStatus, Message, MessageType
from core.boundaries import BOUNDARIES, AgentRole
from models.agent import AgentModel
from services.agents.manager_agent import ManagerAgent
from services.agents.researcher_agent import ResearcherAgent
from services.agents.qa_agent import QAAgent
from core.logging_config import logger

class SwarmOrchestrator:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.connections: List[Callable] = []
        
        self.manager = ManagerAgent(AgentModel(name="Alice", role=AgentRole.MANAGER, permissions=BOUNDARIES[AgentRole.MANAGER]))
        self.researcher = ResearcherAgent(AgentModel(name="Bob", role=AgentRole.RESEARCHER, permissions=BOUNDARIES[AgentRole.RESEARCHER]))
        self.qa = QAAgent(AgentModel(name="Charlie", role=AgentRole.QA, permissions=BOUNDARIES[AgentRole.QA]))

    async def register_connection(self, callback: Callable):
        self.connections.append(callback)

    async def broadcast(self, message: Message):
        for conn in self.connections:
            await conn(message.model_dump_json())

    async def submit_task(self, description: str) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(id=task_id, description=description)
        self.tasks[task_id] = task
        asyncio.create_task(self.run_swarm(task))
        return task

    async def run_swarm(self, task: Task):
        task.status = TaskStatus.IN_PROGRESS
        logger.info(f"Task {task.id} started")
        
        # Simulating swarm conversation
        msg1 = Message(id=str(uuid.uuid4()), from_agent="System", to_agent="Manager", content=f"New task: {task.description}", message_type=MessageType.SYSTEM)
        await self.broadcast(msg1)
        task.conversation_log.append(msg1)
        await asyncio.sleep(1)

        msg2 = await self.manager.process_message(msg1, task.conversation_log)
        await self.broadcast(msg2)
        task.conversation_log.append(msg2)
        await asyncio.sleep(1)

        msg3 = await self.researcher.process_message(msg2, task.conversation_log)
        await self.broadcast(msg3)
        task.conversation_log.append(msg3)
        await asyncio.sleep(1)

        msg4 = await self.qa.process_message(msg3, task.conversation_log)
        await self.broadcast(msg4)
        task.conversation_log.append(msg4)
        
        task.status = TaskStatus.COMPLETED
        logger.info(f"Task {task.id} completed")
        msg_end = Message(id=str(uuid.uuid4()), from_agent="System", to_agent="All", content="Task Completed", message_type=MessageType.SYSTEM)
        await self.broadcast(msg_end)

swarm_orchestrator = SwarmOrchestrator()
