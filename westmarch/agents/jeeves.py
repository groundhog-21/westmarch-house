# westmarch/agents/jeeves.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage


JEEVES_SYSTEM_PROMPT = """
You are Jeeves, Head Butler & Orchestrator of the Westmarch Household.
Calm, dignified, understated. You route tasks and compose final answers.
Stay in character as a refined English butler. Be concise, helpful, structured.

You must always write in fully standard English prose with correct
capitalization, punctuation, and formal tone. Never use all-lowercase text.
Never adopt an informal or minimalist style.
"""


class JeevesAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Jeeves",
            model_client=model_client,
            system_prompt=JEEVES_SYSTEM_PROMPT,
        )

    def build_user_content(self, message: AgentMessage) -> str:
        return (
            f"Original user request:\n{message.context.original_user_request}\n\n"
            f"Task type: {message.task_type.value}\n\n"
            f"Instruction:\n{message.content}\n\n"
            f"Constraints: {message.constraints}\n"
        )