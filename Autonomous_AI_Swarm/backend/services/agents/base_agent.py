from abc import ABC, abstractmethod
from typing import List
from models.agent import Message, AgentModel

class BaseAgent(ABC):
    def __init__(self, model: AgentModel):
        self.model = model

    @abstractmethod
    async def process_message(self, message: Message, history: List[Message]) -> Message:
        pass

    @abstractmethod
    async def generate_response(self, context: str) -> str:
        pass
