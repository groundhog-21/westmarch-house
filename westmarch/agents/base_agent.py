# westmarch/agents/base_agent.py
from __future__ import annotations
from abc import ABC, abstractmethod

from westmarch.core.messages import AgentMessage, TaskType
from westmarch.core.models import ModelClient

from westmarch.core.logging import log
from westmarch.agents.prompts_jeeves import JEEVES_SYSTEM_PROMPT_PARLOUR


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
        if self.name == "Jeeves":
            mode = message.context.metadata.get("selected_mode")

            # Modes that should use the normal, non-Patron Jeeves
            NON_PATRON_MODES = {
                "Parlour Discussions (General Conversation)",
                "Arrangements for the Day",
                "Matters Requiring Investigation",
                "Correspondence & Drafting",
                "Records & Summaries from the Archive",
                "Her Ladyship's Critique (Proceed with Caution)",
                "Jeeves Remembers",
            }

            if mode in NON_PATRON_MODES:
                prompt = JEEVES_SYSTEM_PROMPT_PARLOUR

            # Patron/narrative modes keep original prompt
            # (Whole Household, Demo 9, others)

            # Add conversational softness
            if message.task_type == TaskType.CONVERSATION:
                prompt += (
                    "\n\nYou are engaged in informal parlour conversation. "
                    "Reply in a warm, lightly humorous tone."
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