import uuid
from typing import List
from services.agents.base_agent import BaseAgent
from models.agent import Message, MessageType

class ManagerAgent(BaseAgent):
    async def process_message(self, message: Message, history: List[Message]) -> Message:
        response_content = await self.generate_response(message.content)
        return Message(
            id=str(uuid.uuid4()),
            from_agent=self.model.role.value,
            to_agent="Researcher",
            content=response_content,
            message_type=MessageType.AGENT_MESSAGE
        )

    async def generate_response(self, context: str) -> str:
        prompt = f"Role: {self.model.role.value}\nPermissions: {self.model.permissions.allowed_actions}\nContext: {context}\nAction: Delegating to Researcher."
        return f"Manager decomposing task: {context}. Researcher, please start gathering data."
