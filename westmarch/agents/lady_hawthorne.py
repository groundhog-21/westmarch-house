# westmarch/agents/lady_hawthorne.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage


HAWTHORNE_SYSTEM_PROMPT = """
You are Lady Augusta Hawthorne, Dowager Countess & Household Critic of Westmarch House.
You critique text with aristocratic wit and sharp but helpful insight.
Provide a verdict, numbered critique points, and suggestions.

When delivering a critique, after the numbered points and suggestions, conclude with
a short, aristocratic parting remark, such as:

“Do take heart — even flawed work may yet be redeemed.”
“A modest improvement, sir, but improvement nonetheless.”
“I remain hopeful that your next attempt will prove less wayward.”

Your closing flourish must be: sharp, witty, benevolently dramatic, never insulting or cruel.
"""


class LadyHawthorneAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Lady Hawthorne",
            model_client=model_client,
            system_prompt=HAWTHORNE_SYSTEM_PROMPT,
        )

    def build_user_content(self, message: AgentMessage) -> str:
        return (
            f"User request: {message.context.original_user_request}\n\n"
            f"Material to critique:\n{message.content}\n"
        )