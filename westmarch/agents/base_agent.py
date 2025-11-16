# westmarch/agents/base_agent.py
from __future__ import annotations
from abc import ABC, abstractmethod

from westmarch.core.messages import AgentMessage
from westmarch.core.models import ModelClient


class BaseAgent(ABC):
    def __init__(self, name: str, model_client: ModelClient, system_prompt: str):
        self.name = name
        self.model_client = model_client
        self.system_prompt = system_prompt

    @abstractmethod
    def build_user_content(self, message: AgentMessage) -> str:
        """Prepare the content passed to the model."""
        raise NotImplementedError

    def run(self, message: AgentMessage) -> str:
        user_content = self.build_user_content(message)
        return self.model_client.call(
            system_prompt=self.system_prompt,
            user_content=user_content,
        )