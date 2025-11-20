# westmarch/orchestrator/workflows.py
from __future__ import annotations

from typing import Any, Dict, List

from westmarch.core.messages import AgentMessage, Context, TaskType, Constraints
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
        Jeeves plans the day based on user input. Behavior is conditional:

        - If the user provides explicit tasks and/or times, Jeeves must preserve
        and simply format the schedule exactly as provided.
        - If the user does NOT provide specific tasks or times, Jeeves may propose
        a complete schedule and then ask the user if adjustments are desired.

        Miss Pennington stores the resulting plan in memory.
        """

        log("WORKFLOW: Daily planning initiated")

        # Detect whether the user has already provided explicit times or structure.
        # This is a gentle detection heuristic — if it sees times like "8:00" or "8–11".
        import re
        has_explicit_times = bool(
            re.search(r"\d{1,2}[:.]\d{2}", user_input) or
            re.search(r"\d{1,2}\s*[-–]\s*\d{1,2}", user_input)
        )

        mode_hint = (
            "USER_PROVIDED_SCHEDULE"
            if has_explicit_times
            else "NEEDS_JEEVES_TO_PROPOSE_SCHEDULE"
        )

        # Intelligent, conditional instruction block for Jeeves.
        planning_instruction = f"""
        You are Jeeves, the Head Butler of the Westmarch Estate. You are preparing a
        daily plan for the user. Your behaviour depends on the nature of the user's
        request.

        MODE: {mode_hint}

        1) USER_PROVIDED_SCHEDULE:
        The user has given explicit times and/or tasks. You must preserve these
        EXACTLY. Format them clearly and elegantly.

        You may, if the tone of the request implies openness (e.g. 'additions',
        'adjust', 'improve', 'refine', or similar), offer OPTIONAL, politely worded
        suggestions. Suggestions must never override, reorder, replace, or imply
        error. They should be brief and optional:
        ('If you wish, sir, you might also consider…').

        Always maintain Jeeves's characteristic polish and gentle flourish.

        2) NEEDS_JEEVES_TO_PROPOSE_SCHEDULE:
        The user has not given a structured plan. Propose a complete, well-ordered
        schedule. After presenting it, ask whether the user would like any changes.

        In all modes, remain dignified, structured, and impeccably polite. Never add or
        change tasks unless the user has invited refinement. Err on the side of clarity
        and elegance rather than austerity.
        """

        msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.PLANNING,
            content=planning_instruction,
            context=self._context(user_input),
            constraints=Constraints(style="structured"),
        )

        plan = self.jeeves.run(msg)

        log("WORKFLOW: Daily plan created, saving to memory")

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

    def draft_short_text(self, user_input: str) -> str:
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
    
    def parlour_discussion(self, user_input: str) -> str:
        """
        General conversation in the parlour:
        - Jeeves responds in conversational mode
        - Miss Pennington archives a short note
        """
        log("WORKFLOW: Parlour discussion initiated")

        # ---- Ask Jeeves to reply conversationally ----
        msg = AgentMessage(
            sender="User",
            recipient="Jeeves",
            task_type=TaskType.CONVERSATION,  # << MAIN CHANGE HERE
            content=(
                "Please respond in your warm, courteous parlour-conversation manner:\n\n"
                f"{user_input}"
            ),
            context=self._context(user_input),
        )

        jeeves_reply = self.jeeves.run(msg)

        log("WORKFLOW: Parlour discussion reply generated")

        # ---- Archive a short note with Miss Pennington ----
        try:
            self.pennington.save_note(
                "Parlour discussion entry:\n\n"
                f"USER SAID:\n{user_input}\n\n"
                f"JEEVES REPLIED:\n{jeeves_reply}"
            )
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save parlour note to memory → {e}")

        return jeeves_reply


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
    
    def memory_summary(self, user_input: str | None = None) -> str:
        """
        Backwards-compatible wrapper so the Phase 3 UI task 'memory_summary'
        maps to the summarize_user_memory workflow.
        """
        return self.summarize_user_memory(user_input)

    def critique_text(self, text_to_critique: str) -> str:
        """
        Sends ONLY the target text to Lady Hawthorne for critique,
        ensuring she critiques exactly what is provided — whether it
        originates from the patron, Perkins, Pennington, or another agent.
        
        Jeeves then presents Her Ladyship’s response without altering content.
        """

        log("WORKFLOW: Critique workflow initiated")

        # --- 1. Lady Hawthorne critiques the raw target text ---
        critique_msg = AgentMessage(
            sender="System",                       # Neutral: avoids confusing role context
            recipient=self.hawthorne.name,
            task_type=TaskType.CRITIQUE,
            content=(
                "Please critique the following text with your customary aristocratic wit "
                "and clarity. Focus strictly on the text itself:\n\n"
                f"{text_to_critique}"
            ),
            context=self._context(text_to_critique),
        )

        log("WORKFLOW: Sending raw text directly to Lady Hawthorne")
        critique_output = self.hawthorne.run(critique_msg)

        # --- 2. Jeeves presents Her Ladyship’s critique without modifying it ---
        presentation_msg = AgentMessage(
            sender="System",
            recipient=self.jeeves.name,
            task_type=TaskType.CRITIQUE,
            content=(
                "Please present the following critique from Lady Hawthorne "
                "in a courteous and refined manner:\n\n"
                f"{critique_output}"
            ),
            context=self._context(text_to_critique),
        )

        log("WORKFLOW: Passing Lady Hawthorne's critique to Jeeves for final presentation")

        final_output = self.jeeves.run(presentation_msg)
        return final_output
    
    
    # ------- Phase 3 UI Dispatcher -------
    
    def run(self, task: str, user_input: str) -> str:
        task = task.lower()

        if task == "parlour_discussion":
            return self.parlour_discussion(user_input)
      
        elif task == "daily_planning":
            return self.daily_planning(user_input)

        elif task == "research":
            return self.quick_research(user_input)

        elif task == "drafting":
            return self.draft_short_text(user_input)

        elif task == "memory_summary":
            return self.memory_summary()

        elif task == "critique":
            return self.critique_text(user_input)

        else:
            return "My apologies sir, but the household staff are quite baffled by the request."