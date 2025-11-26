# westmarch/agents/jeeves.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.agents.prompts_jeeves import (
    JEEVES_SYSTEM_PROMPT_MAIN,
    JEEVES_SYSTEM_PROMPT_PARLOUR,
)

from westmarch.core.messages import AgentMessage


class JeevesAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Jeeves",
            model_client=model_client,
            system_prompt=JEEVES_SYSTEM_PROMPT_MAIN,
        )

    def build_user_content(self, message: AgentMessage) -> str:
        """
        Jeeves: Structured task instructions must override persona.
        This method constructs the final user message sent to the LLM.
        """

        parts = []

        # 1. Task context (lightweight metadata)
        parts.append(f"Task: {message.task_type.value}\n")

        # 2. Include original user request if present
        if message.context and message.context.original_user_request:
            parts.append(
                "User Request:\n"
                f"{message.context.original_user_request}\n"
            )

        # 3. THE KEY OVERRIDE
        # Present the instruction as the final directive
        # This ensures the model treats it as dominant.
        parts.append(
            "YOU MUST FOLLOW THE INSTRUCTION BELOW EXACTLY AND LITERALLY. "
            "IT OVERRIDES ALL PRIOR CONTEXT, PERSONA, AND CONVERSATION:\n\n"
            f"{message.content}\n"
        )

        return "\n".join(parts)