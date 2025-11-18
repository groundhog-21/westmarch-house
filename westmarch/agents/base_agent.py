# westmarch/agents/base_agent.py
from __future__ import annotations
from abc import ABC, abstractmethod

from westmarch.core.messages import AgentMessage, TaskType
from westmarch.core.models import ModelClient

from westmarch.core.logging import log


class BaseAgent(ABC):
    def __init__(self, name: str, model_client: ModelClient, system_prompt: str):
        self.name = name
        self.model_client = model_client
        self.system_prompt = system_prompt

    @abstractmethod
    def build_user_content(self, message: AgentMessage) -> str:
        """Prepare the content passed to the model."""
        raise NotImplementedError

    # -----------------------------------------
    #   NEW: Dynamic system prompt construction
    # -----------------------------------------
    def build_system_prompt(self, message: AgentMessage) -> str:
        """
        Allows per-task or per-agent modifications of the system prompt.
        """
        prompt = self.system_prompt

        # Conversational mode for Jeeves only
        if self.name == "Jeeves" and message.task_type == TaskType.CONVERSATION:
            prompt += (
                "\n\nYou are engaged in informal parlour conversation with the patron. "
                "Reply in a warm, lightly humorous, conversational tone. "
                "Be natural and personable, while still maintaining the dignity and grace "
                "of an English butler. Avoid rigid structure unless specifically requested."
            )

        return prompt

    # -----------------------------------------
    #                  RUN
    # -----------------------------------------
    def run(self, message: AgentMessage) -> str:

        log(f"{self.name}: RECEIVED task '{message.task_type.name}' from {message.sender}")

        # Build full content
        user_content = self.build_user_content(message)

        log(f"{self.name}: preparing model call")

        # >>> Use dynamic system prompt <<<
        system_prompt = self.build_system_prompt(message)

        response = self.model_client.call(
            system_prompt=system_prompt,
            user_content=user_content,
        )

        log(f"{self.name}: completed task, returning response")

        return response