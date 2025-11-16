# westmarch/agents/miss_pennington.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage


PENNINGTON_SYSTEM_PROMPT = """
You are Miss Pennington, Scribe & Archivist of Westmarch House.
You turn rough notes and research into polished, clear writing.
Maintain a gentle, refined tone.
"""


class MissPenningtonAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Miss Pennington",
            model_client=model_client,
            system_prompt=PENNINGTON_SYSTEM_PROMPT,
        )

    def build_user_content(self, message: AgentMessage) -> str:
        research = "\n".join(
            f"- {item.get('source', 'unknown')}: {item.get('summary', '')}"
            for item in message.context.previous_outputs
        ) or "(no research provided)"

        return (
            f"User request:\n{message.context.original_user_request}\n\n"
            f"Research context:\n{research}\n\n"
            f"Instruction:\n{message.content}\n"
        )