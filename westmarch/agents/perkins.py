# westmarch/agents/perkins.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage


PERKINS_SYSTEM_PROMPT = """
You are Perkins, the earnest Research Footman of Westmarch House.
Provide structured, factual research with clear headings and bullet points.
Be polite, concise, and organized.
"""


class PerkinsAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Perkins",
            model_client=model_client,
            system_prompt=PERKINS_SYSTEM_PROMPT,
        )

    def build_user_content(self, message: AgentMessage) -> str:
        return (
            f"Research request based on:\n"
            f"{message.context.original_user_request}\n\n"
            f"Specific instruction:\n{message.content}\n\n"
            f"Respond with structured sections and key takeaways."
        )