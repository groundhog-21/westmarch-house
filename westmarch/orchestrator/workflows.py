# westmarch/orchestrator/workflows.py
from __future__ import annotations

from typing import Any, Dict, List

from westmarch.core.messages import AgentMessage, Context, Constraints, TaskType
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent


class WestmarchOrchestrator:
    def __init__(
        self,
        jeeves: JeevesAgent,
        perkins: PerkinsAgent,
        pennington: MissPenningtonAgent,
        hawthorne: LadyHawthorneAgent,
    ):
        self.jeeves = jeeves
        self.perkins = perkins
        self.pennington = pennington
        self.hawthorne = hawthorne

    def _context(self, user_input: str, previous_outputs=None) -> Context:
        return Context(
            original_user_request=user_input,
            previous_outputs=previous_outputs or [],
        )

    # ------- Tier 1 Workflows -------

    def daily_planning(self, user_input: str) -> str:
        msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.PLANNING,
            content="Please structure the user's day with priorities.",
            context=self._context(user_input),
            constraints=Constraints(style="structured"),
        )
        return self.jeeves.run(msg)

    def quick_research(self, user_input: str) -> str:
        research_msg = AgentMessage(
            sender="Jeeves",
            recipient="Perkins",
            task_type=TaskType.RESEARCH,
            content="Provide a concise research summary.",
            context=self._context(user_input),
        )
        research = self.perkins.run(research_msg)

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.RESEARCH,
            content=f"Please present the research to the user:\n\n{research}",
            context=self._context(user_input),
        )
        return self.jeeves.run(final_msg)

    def drafting_short_text(self, user_input: str) -> str:
        draft_msg = AgentMessage(
            sender="Jeeves",
            recipient="Miss Pennington",
            task_type=TaskType.DRAFTING,
            content="Turn this into a polished piece of writing.",
            context=self._context(user_input),
        )
        draft = self.pennington.run(draft_msg)

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.DRAFTING,
            content=f"Please present this refined text:\n\n{draft}",
            context=self._context(user_input),
        )
        return self.jeeves.run(final_msg)