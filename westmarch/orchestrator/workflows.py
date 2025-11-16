# westmarch/orchestrator/workflows.py
from __future__ import annotations

from typing import Any, Dict, List

from westmarch.core.messages import AgentMessage, Context, TaskType
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent

from westmarch.core.logging import log


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
        """
        Jeeves plans the day. Miss Pennington stores the plan in memory.
        """
        log("WORKFLOW: Daily planning initiated")  # <<< NEW

        msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.PLANNING,
            content="Please structure the user's day with priorities.",
            context=self._context(user_input),
            constraints=Constraints(style="structured"),
        )
        plan = self.jeeves.run(msg)

        log("WORKFLOW: Daily plan created, saving to memory")  # <<< NEW

        # Save the plan in Pennington's memory
        self.pennington.save_note(
            f"Daily plan created based on user request:\n\n"
            f"REQUEST:\n{user_input}\n\nPLAN:\n{plan}"
        )

        return plan

    def quick_research(self, user_input: str) -> str:
        """
        Perkins researches; Jeeves presents; Miss Pennington archives the result.
        """
        log("WORKFLOW: Quick research pipeline initiated")  # <<< NEW

        research_msg = AgentMessage(
            sender="Jeeves",
            recipient="Perkins",
            task_type=TaskType.RESEARCH,
            content="Provide a concise research summary.",
            context=self._context(user_input),
        )

        log("WORKFLOW: Passing research task to Perkins")  # <<< NEW

        research = self.perkins.run(research_msg)

        log("WORKFLOW: Research completed, archiving in memory")  # <<< NEW

        # Archive the research
        self.pennington.save_note(
            f"Research performed for user request:\n\n"
            f"REQUEST:\n{user_input}\n\nRESEARCH SUMMARY:\n{research}"
        )

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.RESEARCH,
            content=f"Please present the research to the user:\n\n{research}",
            context=self._context(user_input),
        )

        log("WORKFLOW: Handing research result to Jeeves for presentation")  # <<< NEW

        return self.jeeves.run(final_msg)

    def drafting_short_text(self, user_input: str) -> str:
        """
        Miss Pennington drafts; Jeeves presents; Pennington archives the draft.
        """
        log("WORKFLOW: Drafting workflow initiated")  # <<< NEW

        draft_msg = AgentMessage(
            sender="Jeeves",
            recipient="Miss Pennington",
            task_type=TaskType.DRAFTING,
            content="Turn this into a polished piece of writing.",
            context=self._context(user_input),
        )

        log("WORKFLOW: Sending drafting task to Miss Pennington")  # <<< NEW

        draft = self.pennington.run(draft_msg)

        log("WORKFLOW: Draft completed, saving to memory")  # <<< NEW

        # Archive the drafted text
        self.pennington.save_note(
            f"Drafted text based on user request:\n\n"
            f"REQUEST:\n{user_input}\n\nDRAFT:\n{draft}"
        )

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.DRAFTING,
            content=f"Please present this refined text:\n\n{draft}",
            context=self._context(user_input),
        )

        log("WORKFLOW: Passing refined draft to Jeeves for presentation")  # <<< NEW

        return self.jeeves.run(final_msg)
    
    # ------- Memory-centric Workflow -------

    def summarize_user_memory(self, user_input: str | None = None) -> str:
        """
        Ask Miss Pennington to summarize everything she knows so far,
        then have Jeeves present it gracefully to the user.
        """
        log("WORKFLOW: Memory summary requested")  # <<< NEW

        summary = self.pennington.summarize_memory()

        log("WORKFLOW: Memory summary created, passing to Jeeves")  # <<< NEW

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.PLANNING,
            content=(
                "Please present this as a brief summary of what the household "
                "currently remembers about the patron:\n\n"
                f"{summary}"
            ),
            context=self._context(user_input or "Summarize what you know about me so far."),
        )
        return self.jeeves.run(final_msg)
    
    def critique_text(self, text: str) -> str:
        """
        Lady Hawthorne critiques the given text with her aristocratic wit.
        """

        log("WORKFLOW: Critique workflow initiated")

        # 1. Create the message for Lady Hawthorne
        critique_msg = AgentMessage(
            sender=self.jeeves.name,
            recipient=self.hawthorne.name,
            task_type=TaskType.CRITIQUE,
            content=text,
            context=Context(
                original_user_request=text,
                previous_outputs=[]
            )
        )

        # 2. Send to Lady Hawthorne
        log("WORKFLOW: Sending text to Lady Hawthorne for critique")
        critique = self.hawthorne.run(critique_msg)

        # 3. Allow Jeeves to compose a refined, presentable response
        log("WORKFLOW: Passing critique to Jeeves for presentation")

        summary_msg = AgentMessage(
            sender="System",
            recipient=self.jeeves.name,
            task_type=TaskType.CRITIQUE,
            content=critique,
            context=Context(
                original_user_request=f"Critique this text: {text}",
                previous_outputs=[{"summary": critique}]
            )
        )

        final_output = self.jeeves.run(summary_msg)
        return final_output