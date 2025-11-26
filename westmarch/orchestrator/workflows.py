# westmarch/orchestrator/workflows.py

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

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

    def _context(self, user_input: str, previous_outputs=None, selected_mode: str = None) -> Context:
        return Context(
            original_user_request=user_input,
            previous_outputs=previous_outputs or [],
            selected_mode=selected_mode,
        )

    # ------- Tier 1 Workflows -------

    # ---------------------------------------------------------
    # For memory recall
    # ---------------------------------------------------------

    DOMAIN_KEYWORDS = {
        # Literary & creative writing
        "poetry": [
            "poem", "poetry", "verse", "stanza", "line", "couplet", "sonnet",
            "metaphor", "imagery", "languid moon"
        ],

        # Financial topics
        "finance": [
            "finance", "invest", "investing", "investment", "stock", "stocks",
            "market", "fund", "funds", "etf", "etfs", "index fund",
            "mutual fund", "portfolio", "capital"
        ],

        # Gnome incidents & garden mysteries
        "gnome": [
            "gnome", "garden gnome", "waistcoat", "green waistcoat",
            "horticultural", "paving stones", "wandering gnome"
        ],

        # Meteorological queries
        "weather": [
            "weather", "forecast", "rain", "sunny", "cloudy", "wind",
            "temperature", "cold", "warm"
        ],

        # Daily agendas & planning
        "schedule": [
            "plan", "schedule", "agenda", "appointment",
            "calendar", "daily plan", "itinerary"
        ],

        # Drafting & correspondence
        "drafting": [
            "email", "letter", "draft", "compose", "correspondence",
            "write", "rewrite", "note"
        ],

        # Research queries (Perkins)
        "research": [
            "research", "investigate", "investigation", "analysis",
            "summary", "report"
        ],

        # Historical & archival material
        "history": [
            "history", "historical", "estate", "westmarch", "archive", "timeline"
        ],

        # General conversation (parlour interactions)
        "parlour": [
            "parlour", "chat", "conversation", "talk", "discuss"
        ],

        # Critique domain (Lady Hawthorne)
        "critique": [
            "critique", "review", "appraisal", "assessment"
        ],

        # Sports (new domain per your instruction)
        "sports": [
            "sport", "sports", "tennis", "match", "tournament",
            "score", "set", "athlete", "competition"
        ]
    }

    @staticmethod
    def infer_domains(text: str) -> set:
        """
        Infer semantic domains from a block of text.

        Improvements:
        - Handles multi-word phrases cleanly.
        - Uses whole-word matching for single tokens.
        - Normalizes text for consistent comparisons.
        """
        t = text.lower()

        # Normalized token set for whole-word matching
        tokens = set(t.replace(",", " ").replace(".", " ").split())

        found: set[str] = set()

        for domain, keywords in WestmarchOrchestrator.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                kw_lower = kw.lower()

                # Case 1: multi-word phrase (“garden gnome”)
                if " " in kw_lower:
                    if kw_lower in t:       # non-fuzzy exact phrase match
                        found.add(domain)
                        break

                # Case 2: single word (“gnome”, “fund”)
                else:
                    if kw_lower in tokens:
                        found.add(domain)
                        break

        return found

    def parlour_discussion(self, user_input: str) -> str:
        """
        General conversation in the parlour.

        - Jeeves responds as conversational butler.
        - Context includes recent memory (parlour notes, staff roster, etc.).
        - Miss Pennington archives a short note in long-term memory.
        """
        log("WORKFLOW: Parlour discussion initiated")

        # Approval / closure detection
        lower = user_input.strip().lower()

        closure_phrases = [
            "thank you",
            "that will do",
            "that will be all",
            "that will suffice",
            "you may go",
            "very good",
            "excellent, thank you",
            "splendid, thank you",
            "most helpful",
            "quite helpful",
            "much obliged",
            "carry on",
            "as you were",
            "that's all jeeves",
            "thank you jeeves",
            "dismissed",
        ]

        if any(p in lower for p in closure_phrases):
            return (
                "Certainly, sir. I shall retire to the wing, "
                "but will attend instantly if called."
            )

        # Build context that includes recent exchanges + memory
        context = self._context(user_input)

        instruction = (
            "You are Jeeves, Head Butler of the Westmarch Estate, conversing "
            "with the Master in the parlour.\n"
            "Respond in your warm, courteous, but still understated manner.\n\n"
            "You may, when it is natural, draw upon prior notes or memory entries "
            "included in the context (for example earlier conversations, the "
            "household staff roster, or notable projects recorded by Miss Pennington).\n"
            "Use memory for gentle continuity only: brief references such as "
            "\"As we discussed yesterday\" or recalling known preferences.\n\n"
            "Do NOT invent new household staff or contradict the known roster. "
            "If the user inquires about the staff, describe ONLY the Westmarch "
            "staff you know from your instructions and any roster in memory.\n\n"
            "Now respond to the user's latest remark."
        )

        msg = AgentMessage(
            sender="User",
            recipient="Jeeves",
            task_type=TaskType.CONVERSATION,
            content=f"{instruction}\n\nUSER SAID:\n{user_input}",
            context=context,
        )

        jeeves_reply = self.jeeves.run(msg)
        log("WORKFLOW: Parlour discussion reply generated")

        # Archive the exchange via Miss Pennington as a parlour log entry
        try:
            self.pennington.save_note(
                "Parlour discussion entry:\n\n"
                f"USER SAID:\n{user_input}\n\n"
                f"JEEVES REPLIED:\n{jeeves_reply}"
            )
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save parlour note to memory → {e}")

        return jeeves_reply

    def daily_planning(self, user_input: str, selected_mode: str = None) -> str:
        """
        Jeeves plans the day based on user input. Behavior is conditional:

        - If the user provides explicit tasks and/or times, Jeeves must preserve
        and simply format the schedule exactly as provided.
        - If the user does NOT provide specific tasks or times, Jeeves may propose
        a complete schedule and then ask the user if adjustments are desired.

        Additionally:
        - If the user expresses approval (e.g. "This will do nicely"), the workflow stops
        and Jeeves gives a short acknowledgement rather than generating a new schedule.

        Miss Pennington stores the resulting plan in memory.
        """

        log("WORKFLOW: Daily planning initiated")

        # -------------------------------------------------------------
        # 1. Detect approval (stop condition)
        # -------------------------------------------------------------
        approval_phrases = [
            "thank you",
            "that will be all",
            "this will do nicely",
            "that will do nicely",
            "this looks good",
            "that looks good",
            "perfect",
            "excellent",
            "very good",
            "that will do",
            "this will do",
            "thank you, jeeves"
        ]

        lower_input = user_input.lower()

        if any(phrase in lower_input for phrase in approval_phrases):
            confirmation = (
                "Very good, sir. I shall see that everything is arranged accordingly. "
                "Do let me know if you require any further adjustments."
            )

            # Save the approval as a finalized-plan memory entry
            try:
                self.pennington.save_note(
                    f"Daily plan finalized:\n\nUSER APPROVAL:\n{user_input}"
                )
            except Exception as e:
                log(f"WORKFLOW: Warning – could not save finalized plan → {e}")

            return confirmation

        # -------------------------------------------------------------
        # 2. Detect whether user provided explicit times/tasks
        # -------------------------------------------------------------
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

        # -------------------------------------------------------------
        # 3. Instruction block for Jeeves
        # -------------------------------------------------------------
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
            context = Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode}
            ),
            constraints=Constraints(style="structured"),
        )

        # -------------------------------------------------------------
        # 4. Generate the plan
        # -------------------------------------------------------------
        plan = self.jeeves.run(msg)

        log("WORKFLOW: Daily plan created, saving to memory")

        # Save the plan in Pennington's memory
        try:
            self.pennington.save_note(
                f"Daily plan created based on user request:\n\n"
                f"REQUEST:\n{user_input}\n\nPLAN:\n{plan}"
            )
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save plan to memory → {e}")

        return plan

    def quick_research(self, user_input: str, selected_mode: str = None) -> str:
        """
        Hybrid approach:
        - Perkins performs the research and replies in his own voice.
        - Miss Pennington archives the result in long-term memory.
        - Jeeves remains the orchestrator (he initiates the task and
          defines the context) but does not rewrite the final answer.

        Additionally:
        - If the user clearly expresses satisfaction / closure
          (e.g. “nothing further”, “this is excellent”), we do NOT
          trigger a new research run. Instead Jeeves returns a brief,
          courteous acknowledgement and the workflow stops.
        """

        log("WORKFLOW: Quick research pipeline initiated")

        # ---- 0. Detect “this is fine, we’re done here” ----
        lower = user_input.lower().strip()
        approval_phrases = [
            "thank you",
            "that will do",
            "that will be all",
            "that will suffice",
            "you may go",
            "very good",
            "excellent, thank you",
            "splendid, thank you",
            "most helpful",
            "quite helpful",
            "much obliged",
            "carry on",
            "as you were",
            "that's all perkins",
            "thank you, perkins",
            "dismissed",
        ]

        if any(phrase in lower for phrase in approval_phrases):
            log("WORKFLOW: Detected approval/closure in research mode; no new research call")
            return (
                "At once, sir. I shall retire this matter in the household ledger. "
                "If ever you desire supplementary findings, I am wholly at your disposal."
            )

        # ---- 1. Ask Perkins to perform the research ----
        research_msg = AgentMessage(
            sender="Jeeves",          # Orchestrator initiating the task
            recipient="Perkins",      # Research Footman
            task_type=TaskType.RESEARCH,
            content=(
                "Please provide a concise, well-structured research summary "
                "for the user's request."
            ),
            context=Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode},
            ),
        )

        log("WORKFLOW: Passing research task to Perkins")
        research = self.perkins.run(research_msg)

        # ---- 2. Archive the research in memory via Miss Pennington ----
        log("WORKFLOW: Research completed, archiving in memory")
        try:
            self.pennington.save_note(
                f"Research performed for user request:\n\n"
                f"REQUEST:\n{user_input}\n\nRESEARCH SUMMARY:\n{research}"
            )
            log("WORKFLOW: Research note archived successfully")
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save research note to memory → {e}")

        # ---- 3. Hybrid behaviour: return Perkins’s own words directly ----
        return research

    def draft_short_text(self, user_input: str, selected_mode: str = None) -> str:
        """
        Hybrid approach:
        - Miss Pennington transforms the user's rough notes into polished prose,
          and replies directly in her own voice.
        - The resulting draft is archived in memory.
        - Jeeves remains the orchestrator (he frames the task and context),
          but does not rewrite the draft.
        """

        log("WORKFLOW: Drafting workflow initiated")

        # Closure detection
        lower = user_input.lower().strip()
        approval_phrases = [
            "thank you",
            "that will do",
            "that will be all",
            "that will suffice",
            "you may go",
            "very good",
            "excellent, thank you",
            "splendid, thank you",
            "most helpful",
            "quite helpful",
            "much obliged",
            "carry on",
            "as you were",
            "that's all miss pennington",
            "thank you, miss pennington",
            "dismissed",
        ]

        if any(phrase in lower for phrase in approval_phrases):
            log("WORKFLOW: Detected approval/closure in research mode; no new research call")
            return (
                "Certainly, sir. I will set this matter gently to rest within the ledger. "
                "Whenever fresh words or tidy records are needed, I shall attend at once."
            )
        # Determine whether the user supplied text to rewrite
        user_lower = user_input.lower()

        is_rewrite = any(keyword in user_lower for keyword in [
            "rewrite", "polish", "improve", "edit", "revise",
            "tidy", "fix this", "clean this", "turn this", "rework"
        ])

        if is_rewrite:
            drafting_instruction = (
                "Please transform the user's notes or rough text into a polished, "
                "ready-to-send piece of writing. Do not explain your process; simply "
                "return the finished text."
            )
        else:
            drafting_instruction = (
                "Please compose a polished, concise piece of writing that fulfills the "
                "user's request. Do not explain your process; simply return the final "
                "draft in completed form."
            )

        draft_msg = AgentMessage(
            sender="Jeeves",
            recipient="Miss Pennington",
            task_type=TaskType.DRAFTING,
            content=drafting_instruction,
            context=Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode},
            ),
        )

        log("WORKFLOW: Sending drafting task to Miss Pennington")
        draft = self.pennington.run(draft_msg)

        # Archive the drafted text
        log("WORKFLOW: Draft completed, archiving in memory")
        try:
            self.pennington.save_note(
                f"Drafted text based on user request:\n\n"
                f"REQUEST:\n{user_input}\n\nDRAFT:\n{draft}"
            )
            log("WORKFLOW: Draft note archived successfully")
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save drafted text to memory → {e}")

        # Hybrid: respond in Miss Pennington’s own voice
        return draft

    # ------- Memory-centric Workflow -------

    def query_archive(self, user_input: str, selected_mode: str = None) -> str:
        """
        Query the archive (memory.json) for any notes relevant to the user's request.
        Then ask Miss Pennington to summarise the retrieved content,
        and finally have Jeeves present it elegantly.
        """

        log("WORKFLOW: Archive query initiated")

        # 0. Approval / closure detection
        closing_phrases = [
            "that will suffice",
            "that will do nicely",
            "this will do nicely",
            "splendid",
            "excellent, thank you",
            "my compliments",
            "that will be all"
        ]

        if any(phrase in user_input.lower() for phrase in closing_phrases):
            return (
                "Very good, sir. The archives shall remain at your disposal. "
                "Do let me know if you require anything further."
            )

        # 1. Load all memory
        all_notes = self.pennington.load_all_notes()

        # 2. Perform matching using years prior to 2000 — the perfect filter
        import re

        matches = [
            note for note in all_notes
            if re.search(r"\b(1[0-9]{3})\b", note["content"])
        ]

        # 3. Debug logging
        if not matches:
            log("WORKFLOW: Archive query found NO historical matches")
        else:
            log(f"WORKFLOW: Archive query found {len(matches)} historical matches")
            for idx, note in enumerate(matches, start=1):
                preview = note.get("content", "")[:200].replace("\n", " ")
                tags = note.get("tags", [])
                log(f"WORKFLOW: Historical Match #{idx} | tags={tags} | preview={preview}...")

        # 4. No matches? Inform the patron politely
        if not matches:
            return (
                "I regret to say, sir, that the archives contain no records "
                "relevant to your request. Might you wish to phrase it differently?"
            )

        # 5. Combine matching entries
        combined = "\n\n---\n\n".join(note["content"] for note in matches)

        # 6. Ask Miss Pennington for a refined summary
        log("WORKFLOW: Passing archive texts to Miss Pennington for summarisation")
        summary = self.pennington.summarize_text(
            combined,
            context=Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode},
            ),
        )

        # 7. Have Jeeves present it in his elegant voice
        log("WORKFLOW: Archive summary ready, passing to Jeeves")

        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.CONVERSATION,
            content=(
                "Please present the following as a concise, elegant summary drawn "
                "from the Estate archives:\n\n"
                f"{summary}"
            ),
            context=Context(
                original_user_request=user_input,
                previous_outputs=[],
                metadata={"selected_mode": selected_mode},
            ),
        )

        return self.jeeves.run(final_msg)

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

    def critique_text(self, text_to_critique: str, selected_mode: str = None) -> str:
        """
        Sends ONLY the target text to Lady Hawthorne for critique,
        ensuring she critiques exactly what is provided — whether it
        originates from the patron, Perkins, Pennington, or another agent.

        Hybrid approach:
        - Lady Hawthorne replies in her own voice directly to the user.
        - Jeeves orchestrates the call and memory archiving but does not
        rephrase or wrap her critique.
        """

        log("WORKFLOW: Critique workflow initiated")

        # --- 0. Approval / closure detection ---
        lower = text_to_critique.strip().lower()

        closure_phrases = [
            "thank you",
            "that will do",
            "that will suffice",
            "very well",
            "fine, thank you",
            "fine thank you",
            "excellent, thank you",
            "alright then",
            "okay then",
            "appreciated",
            "much obliged"
        ]

        if any(p in lower for p in closure_phrases):
            return (
                "As you wish, sir. Should further literary agonies ever require my lantern, "
                "I shall of course remain available."
            )

        # --- 1. Ask Lady Hawthorne to critique the raw text ---
        critique_msg = AgentMessage(
            sender="System",   # Neutral: avoids confusing persona context
            recipient=self.hawthorne.name,
            task_type=TaskType.CRITIQUE,
            content=(
                "Please critique the following text with your customary "
                "aristocratic wit and clarity. Focus strictly on the text itself.\n\n"
                "Your critique must be no longer than 3 sentences.\n\n"
                "Always conclude your critique with an encouraging remark.\n\n"
                f"{text_to_critique}"
            ),
                context=Context(
                    original_user_request=text_to_critique,
                    previous_outputs=[],
                    metadata={"selected_mode": selected_mode},
                ),
        )

        log("WORKFLOW: Sending raw text directly to Lady Hawthorne")
        critique_output = self.hawthorne.run(critique_msg)

        # --- 2. Archive the critique in memory (via Pennington) ---
        try:
            self.pennington.save_note(
                "Critique requested from Lady Hawthorne:\n\n"
                f"TEXT:\n{text_to_critique}\n\nCRITIQUE:\n{critique_output}"
            )
            log("WORKFLOW: Critique note archived successfully")
        except Exception as e:
            log(f"WORKFLOW: Warning – could not save critique note to memory → {e}")

        # --- 3. Hybrid: return Her Ladyship’s own words directly ---
        return critique_output
    
    def whole_household(self, user_input: str, selected_mode: str = None) -> str:
        """
        Full multi-agent orchestration workflow.
        """

        log("WORKFLOW: Whole household orchestration initiated")

        # -------------------------------------------------------
        # 0. Approval / Closure Detection
        # -------------------------------------------------------
        lower = user_input.strip().lower()

        closure_phrases = [
            "thank you",
            "my thanks",
            "that will do",
            "that will suffice",
            "very well",
            "fine, thank you",
            "fine thank you",
            "excellent, thank you",
            "alright then",
            "okay then",
            "appreciated",
            "much obliged"
        ]

        if any(p in lower for p in closure_phrases):
            return (
                "Indeed, sir. If another garden ornament develops ambitions of nocturnal adventure, "
                "we shall of course investigate with all due diligence."
            )

        # -------------------------------------------------------
        # 1. Perkins — Structured Investigation
        # -------------------------------------------------------
        research_msg = AgentMessage(
            sender="Jeeves",
            recipient="Perkins",
            task_type=TaskType.RESEARCH,
            content=(
                "Please investigate the user's matter with a concise, structured analysis. "
                "Your report MUST be no more than 120 words. "
                "Use exactly three sections: 'Observation', 'Possible Causes', and 'Most Likely Explanation'. "
                "Use no more than 3 bullet points total. "
                "Avoid long sentences or extended exposition."
            ),
            context=Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode},
            ),
        )

        perkins_output = self.perkins.run(research_msg)

        # Archive
        try:
            self.pennington.save_note(
                f"[Whole Household] Perkins investigation:\nUSER REQUEST:\n{user_input}\n\nOUTPUT:\n{perkins_output}"
            )
        except Exception as e:
            log(f"Warning — could not save Perkins output → {e}")

        # -------------------------------------------------------
        # 2. Lady Hawthorne — Interjects
        # -------------------------------------------------------
        hawthorne_output = self.hawthorne.run(
            AgentMessage(
                sender="System",
                recipient=self.hawthorne.name,
                task_type=TaskType.CRITIQUE,
                content=(
                    "Please offer a brief, aristocratic interjection commenting on Perkins’s investigation. "
                    "Your response must be a SINGLE PARAGRAPH of no more than 80–100 words. "
                    "You may include ONE specific suggested improvement at the end, introduced with the phrase "
                    "'Suggested refinement:' "
                    "Avoid numbered lists, lengthy analysis, or multi-paragraph commentary. "
                    "Maintain Lady Hawthorne’s witty, aristocratic tone but remain concise.\n\n"
                    f"{perkins_output}"
                ),
                context=Context(
                    original_user_request=user_input,
                    metadata={"selected_mode": selected_mode},
                ),
            )
        )

        # -------------------------------------------------------
        # 3. Miss Pennington — Initial Draft
        # -------------------------------------------------------
        pennington_output = self.pennington.run(
            AgentMessage(
                sender="Jeeves",
                recipient="Miss Pennington",
                task_type=TaskType.DRAFTING,
                content=(
                    "Please draft a very short, extremely polite note to the neighbours "
                    "about the unusual movement of the garden gnome. "
                    "Your letter must be no more than 80–100 words total, "
                    "written in 4–5 sentences. "
                    "Avoid flourishes, avoid digressions, and do not include commentary "
                    "outside the letter itself. "
                    "End with a single warm closing line, followed by a signature (“Miss Pennington”).\n\n"
                    "Write only the letter."
                ),
                context=Context(
                    original_user_request=user_input,
                    metadata={"selected_mode": selected_mode},
                ),
            )
        )

        # -------------------------------------------------------
        # 4. Lady Hawthorne critiques Miss Pennington’s letter
        # -------------------------------------------------------
        hawthorne_letter_feedback = self.hawthorne.run(
            AgentMessage(
                sender="System",
                recipient=self.hawthorne.name,
                task_type=TaskType.CRITIQUE,
                content=(
                    "Please critique Miss Pennington’s drafted letter. "
                    "Your critique must be extremely brief: no more than 40–60 words, "
                    "written in 3–5 sentences total. "
                    "Provide exactly ONE specific improvement. "
                    "Do not include lists, rewrites, or lengthy commentary. "
                    "Maintain your aristocratic tone.\n\n"
                    f"{pennington_output}"
                ),
                context=Context(
                    original_user_request=user_input,
                    metadata={"selected_mode": selected_mode},
                ),
            )
        )

        # -------------------------------------------------------
        # 5. Miss Pennington revises the letter
        # -------------------------------------------------------
        pennington_revision = self.pennington.run(
            AgentMessage(
                sender="System",
                recipient="Miss Pennington",
                task_type=TaskType.DRAFTING,
                content=(
                    "Lady Hawthorne has critiqued your draft. Please revise the letter using her "
                    "single suggested improvement. The revised letter must be concise, no more "
                    "than 80–100 words. End the revised letter with a warm closing line and your "
                    "signature (“Miss Pennington”). Avoid ornamentation, ensure the request for "
                    "neighbour observations is clear, and do not add new ideas or repeat content "
                    "from the original draft.\n\n"
                    "Your original draft:\n"
                    f"{pennington_output}\n\n"
                    "Lady Hawthorne said:\n"
                    f"{hawthorne_letter_feedback}"
                ),
                context=Context(
                    original_user_request=user_input,
                    metadata={"selected_mode": selected_mode},
                ),
            )
        )

        # -------------------------------------------------------
        # 6A. Miss Pennington summarises all steps
        # -------------------------------------------------------
        pennington_summary = self.pennington.run(
            AgentMessage(
                sender="System",
                recipient="Miss Pennington",
                task_type=TaskType.DRAFTING,
                content=(
                    "Please produce a concise, elegant summary of the entire multi-agent "
                    "workflow that has just occurred. Your summary must:\n"
                    "• be 180–240 words long\n"
                    "• use ONLY the information explicitly provided below\n"
                    "• include a brief reference to, and a single short quote from, each participant's contribution\n"
                    "• reproduce the FULL TEXT of your revised letter exactly as written, "
                    "  as its own paragraph or block, without paraphrasing or altering any words\n"
                    "• be structured using a separate paragraph for each participant:\n"
                    "     - Perkins’ investigation\n"
                    "     - Lady Hawthorne’s first interjection\n"
                    "     - your initial draft\n"
                    "     - Lady Hawthorne’s critique\n"
                    "     - your revised letter\n"
                    "• maintain your refined, archivist tone (calm, clear, lightly wry)\n"
                    "• avoid adding new theories, invented details, or interpretations\n\n"
                    "Here is the complete record of agent outputs:\n\n"
                    "==== PERKINS' INVESTIGATION ====\n"
                    f"{perkins_output}\n\n"
                    "==== LADY HAWTHORNE'S FIRST REMARK ====\n"
                    f"{hawthorne_output}\n\n"
                    "==== MISS PENNINGTON'S FIRST DRAFT ====\n"
                    f"{pennington_output}\n\n"
                    "==== LADY HAWTHORNE'S CRITIQUE ====\n"
                    f"{hawthorne_letter_feedback}\n\n"
                    "==== MISS PENNINGTON'S REVISION ====\n"
                    f"{pennington_revision}\n\n"
                    "Please now produce your final archival summary."
                ),
                context=Context(
                    original_user_request=user_input,
                    metadata={"selected_mode": selected_mode},
                ),
            )
        )

        # -------------------------------------------------------
        # 6B. Jeeves presents Miss Pennington's summary
        # -------------------------------------------------------
        final_msg = AgentMessage(
            sender="System",
            recipient="Jeeves",
            task_type=TaskType.CONVERSATION,
            content=(
                "Miss Pennington has prepared the final archival summary of the "
                "household’s coordinated investigation. Please present her summary to "
                "the Patron in your polished, understated butler’s voice.\n\n"
                "Guidelines:\n"
                "• Do NOT add new information.\n"
                "• Do NOT reinterpret or expand on the events.\n"
                "• You may introduce her summary with a single courteous line.\n"
                "• Then reproduce her summary verbatim.\n"
                "• Then close with one brief, dignified concluding remark.\n\n"
                f"Here is Miss Pennington’s summary:\n\n{pennington_summary}"
            ),
            context=Context(
                original_user_request=user_input,
                metadata={"selected_mode": selected_mode},
            ),
        )

        return self.jeeves.run(final_msg)

    # -------------------------
    # Memory Recall – Helpers
    # -------------------------

    def _extract_memory_hints(self, user_input: str) -> Dict[str, List[str]]:
        """
        Very lightweight intent extractor for memory recall.
        Returns a dict of keyword and agent hints based on the user's question.
        """
        text = user_input.lower().strip()

        keywords: List[str] = []
        agent_hints: List[str] = []
        topic_hints: List[str] = []
        time_hints: List[str] = []

        # --- Topic / content hints ---
        if "poem" in text or "verse" in text or "stanza" in text:
            keywords.extend([
                "poem",
                "o languid moon",
                "languid moon",
            ])
            topic_hints.append("poem")

        if "gnome" in text or "garden gnome" in text:
            keywords.extend([
                "gnome",
                "garden gnome",
            ])
            topic_hints.append("gnome")

        if "letter" in text or "note" in text or "email" in text:
            keywords.extend([
                "letter",
                "note",
            ])
            topic_hints.append("letter")

        if "critique" in text or "review" in text or "what did she say" in text:
            keywords.append("critique")

        if "plan" in text or "planning" in text or "schedule" in text:
            keywords.append("plan")
            topic_hints.append("planning")

        # --- Agent hints ---
        if "lady hawthorne" in text or "her ladyship" in text or "lady augusta" in text:
            agent_hints.append("lady hawthorne")

        if "perkins" in text:
            agent_hints.append("perkins")

        if "miss pennington" in text or "pennington" in text:
            agent_hints.append("miss pennington")

        if "jeeves" in text:
            agent_hints.append("jeeves")

        # --- Time hints (for possible future use) ---
        if "yesterday" in text:
            time_hints.append("yesterday")
        if "earlier today" in text or "earlier" in text:
            time_hints.append("today")
        if "last week" in text:
            time_hints.append("last week")

        return {
            "keywords": list(dict.fromkeys(keywords)),      # de-duplicated
            "agent_hints": list(dict.fromkeys(agent_hints)),
            "topic_hints": list(dict.fromkeys(topic_hints)),
            "time_hints": list(dict.fromkeys(time_hints)),
        }

    def _find_best_memory_match(
        self,
        hints: Dict[str, List[str]],
        fallback_query: str,
    ) -> Optional[Dict]:
        """
        Given extracted hints, scan Miss Pennington's memory entries and
        pick the single best-matching entry using a simple scoring system.

        If no hints are present, falls back to a direct text search using
        the user's query string.
        """
        # If we have no useful hints at all, fall back to direct search.
        if not (hints["keywords"] or hints["agent_hints"] or hints["topic_hints"]):
            direct_matches = self.pennington.search_memory(fallback_query)
            if not direct_matches:
                return None
            # Choose the most recent direct match
            return max(
                direct_matches,
                key=lambda e: e.get("timestamp", ""),
            )

        # Otherwise, load all notes and score them
        entries = self.pennington.load_all_notes()
        if not entries:
            return None

        best_entry: Optional[Dict] = None
        best_score: int = 0

        for entry in entries:
            content = entry.get("content", "")
            lower = content.lower()
            score = 0

            # Strong matches: primary keywords
            for kw in hints["keywords"]:
                if kw in lower:
                    score += 3

            # Agent mentions
            for ag in hints["agent_hints"]:
                if ag in lower:
                    score += 2

            # Topic hints (weaker)
            for th in hints["topic_hints"]:
                if th in lower:
                    score += 1

            # (Optional future extension: use time_hints with timestamps)

            if score <= 0:
                continue

            if score > best_score:
                best_score = score
                best_entry = entry
            elif score == best_score and best_entry is not None:
                # Tie-breaker: prefer more recent timestamp
                ts_new = entry.get("timestamp", "")
                ts_old = best_entry.get("timestamp", "")
                if ts_new > ts_old:
                    best_entry = entry

        return best_entry

    def recall_memory(self, user_input: str, selected_mode: str = None) -> str:
        """
        Jeeves retrieves past notes from Miss Pennington’s memory ledger
        that relate to the user's query.
        """

        log("WORKFLOW: Memory recall initiated")

        # -----------------------------------------------------
        # 0. Closure / approval detection
        # -----------------------------------------------------
        lower = user_input.strip().lower()

        closure_phrases = [
            "thank you",
            "my thanks",
            "that will do",
            "that will suffice",
            "that will be all",
            "very well",
            "fine, thank you",
            "fine thank you",
            "excellent, thank you",
            "alright then",
            "okay then",
            "appreciated",
            "much obliged",
        ]

        if any(p in lower for p in closure_phrases):
            log("MEMORY-RECALL: Closure phrase detected — Jeeves retires gracefully.")
            return (
                "Indeed, sir. Miss Pennington and I remain prepared "
                "to recover any stray reflections."
            )

        # -----------------------------------------------------
        # 1. Infer domain(s) of the user query
        # -----------------------------------------------------
        log(f"MEMORY-RECALL: Jeeves notes the user's inquiry → '{lower}'")
        log("MEMORY-RECALL: Extracting keywords from query…")
        user_domains = self.infer_domains(lower)
        log(f"MEMORY-RECALL: Jeeves infers query domains → {user_domains}")

        # -----------------------------------------------------
        # 2. Ask Miss Pennington for all notes (raw candidates)
        # -----------------------------------------------------
        log("MEMORY-RECALL: Consulting Miss Pennington’s ledger for candidate entries…")
        all_notes = self.pennington.load_all_notes()  # or whatever your method is called
        log(f"MEMORY: Loaded {len(all_notes)} notes from the ledger")

        # -----------------------------------------------------
        # 3. Score each note against the query
        # -----------------------------------------------------
        def score_entry(content: str, query: str) -> int:
            # Very simple keyword overlap scoring for now
            q_words = set(query.split())
            score = 0
            for w in q_words:
                if w and w in content.lower():
                    score += 1
            return score

        candidates: list[tuple[int, dict]] = []
        for entry in all_notes:
            content = entry.get("content", "") or ""
            s = score_entry(content, lower)
            if s > 0:
                candidates.append((s, entry))

        if not candidates:
            log("MEMORY-RECALL: Alas — no entries contained any of the keywords.")
            return (
                "I have consulted Miss Pennington’s meticulously kept ledger, sir, "
                "but I fear no relevant recollection appears recorded under that description. "
                "If you recall even a fragment more, I should be delighted to search again."
            )

        # Sort by descending score
        candidates.sort(key=lambda pair: pair[0], reverse=True)

        # -----------------------------------------------------
        # 4. Log only the TOP 10 candidates
        # -----------------------------------------------------
        top_candidates = candidates[:10]
        top_best_score = top_candidates[0][0]
        log(f"MEMORY-RECALL: Highest scoring entry achieves → {top_best_score}")
        log("MEMORY-RECALL: Showing top 10 candidates by score:")

        for score, entry in top_candidates:
            snippet = (entry.get("content", "") or "").replace("\n", " ")
            if len(snippet) > 80:
                snippet = snippet[:80] + "…"
            log(f"MEMORY-RECALL: • score {score:2d} → {snippet}")

        # -----------------------------------------------------
        # 5. Apply strict domain prioritization (on top 10 only)
        # -----------------------------------------------------
        log("MEMORY-RECALL: Checking for domain coherence (finance, poetry, gnomes)…")

        chosen_entry: Optional[dict] = None

        for score, entry in top_candidates:
            content = entry.get("content", "") or ""
            entry_domains = self.infer_domains(content)
            log(f"MEMORY-RECALL: Ledger entry domains → {entry_domains}")

            # Domain logic:
            # - If user_domains is empty, allow anything.
            # - If entry has no domains, allow it (fallback).
            # - Otherwise, require intersection.
            if not user_domains or not entry_domains or (user_domains & entry_domains):
                chosen_entry = entry
                log("MEMORY-RECALL: A suitable recollection has been selected for presentation.")
                break

        # If no domain-coherent entry found among top 10,
        # fall back to the single best-scoring candidate overall.
        if chosen_entry is None:
            _, chosen_entry = top_candidates[0]
            log("MEMORY-RECALL: No domain-coherent candidate found; "
                "falling back to the highest-scoring entry.")

        log("MEMORY-RECALL: --- END OF MEMORY RECALL WORKFLOW ---")

        # -----------------------------------------------------
        # 6. Produce Jeeves's reply
        # -----------------------------------------------------
        content = (chosen_entry.get("content", "") or "").strip()

        return (
            "Indeed, sir. Upon consulting Miss Pennington’s carefully kept ledger, "
            "I find the following relevant recollection:\n\n"
            f"{content}\n\n"
            "If you wish to revisit any other matter, I shall be glad to search the ledger again."
        )
    
    # ------- FOR DEMO 9 -------

    def _make_msg(self, sender: str, recipient: str, task: TaskType, content: str) -> AgentMessage:
        return AgentMessage(
            sender=sender,
            recipient=recipient,
            task_type=task,
            content=content,
            context=Context(
                original_user_request=None,
                previous_outputs=[],
                metadata={},
            ),
            constraints=Constraints(),  # default OK
        )
    
    def _run_archival_metadata_scrutinizer(self) -> str:
        """
        Custom tool: Archival Metadata Scrutinizer v3.2

        For demo purposes, this is deterministic and does not call the model.
        You can of course make this smarter if you like.
        """
        return (
            "Ink dated 1847.\n"
            "Tremor frequency: pronounced.\n"
            "Foreign substances: biscuit crumbs (0.7 g).\n"
            "Ambient dread: moderate."
        )

    def run_archive_mystery(self) -> list[dict]:
        """
        Demo 9 – Stage 1 Test
        Using REAL AgentMessage objects, no system_message hacks.
        """

        from westmarch.core.messages import AgentMessage, TaskType, Context, Constraints

        messages: list[dict] = []

        # Helper: create consistent message objects
        def make_message(sender: str, recipient: str, task: TaskType, content: str) -> AgentMessage:
            return AgentMessage(
                sender=sender,
                recipient=recipient,
                task_type=task,
                content=content,
                context=Context(
                    original_user_request=None,
                    previous_outputs=[],
                    metadata={},
                ),
                constraints=Constraints(),
            )

        # Helper: add to UI message list
        def add_ui(role: str, speaker: str, content: str):
            messages.append(
                {
                    "role": role,     # "assistant" or "user"
                    "speaker": speaker,
                    "content": content,
                }
            )

        # -----------------------------
        # NARRATOR STYLE STANDARD
        # -----------------------------
        # The narrator provides atmospheric, external description ONLY.
        # The narrator must not:
        # - describe thoughts, feelings, motives, or intentions of any entity
        # - personify the iron door beyond purely physical behavior
        # - interpret sounds or movements as sentient or deliberate
        # - imply unseen forces, awareness, emotion, or judgement
        # The narrator may:
        # - describe light, sound, movement, stillness
        # - describe environmental changes and sensory details
        # - set tone through external observation alone

        # -----------------------------
        # STAGE 1 – Pennington Intro
        # -----------------------------

        # 1. Pennington discovers the parchment
        pennington_intro_instruction = (
            "Address the Patron and explain that while indexing the archives, "
            "you discovered a parchment misfiled under "
            "'Agricultural Affairs → Troublingly Damp Potatoes'. "
            "Keep it to 2–3 sentences."
        )
        pennington_intro_msg = make_message(
            sender="Jeeves",           # orchestrator proxy
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_intro_instruction,
        )
        pennington_intro = self.pennington.run(pennington_intro_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington: {pennington_intro}",
        )

        # 2. Scripted user reply
        add_ui(
            role="user",
            speaker="user",
            content="👤 User: What sort of parchment is it?",
        )

        # 3. Pennington follow-up
        pennington_follow_instruction = (
            "Explain briefly that the parchment is labelled "
            "'UNEXPLAINED RATTLING — DO NOT DISTURB'. Stay in character and concise."
        )
        pennington_follow_msg = make_message(
            sender="Jeeves",
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_follow_instruction,
        )
        pennington_follow = self.pennington.run(pennington_follow_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington: {pennington_follow}",
        )

        # 4. Jeeves reaction
        jeeves_instruction = (
            "React to Miss Pennington's discovery with mild interest and state "
            "that you will summon Perkins."
        )
        jeeves_msg = make_message(
            sender="Miss Pennington",   # naturalistic sender
            recipient="Jeeves",
            task=TaskType.CONVERSATION,  # conversational tone for Jeeves
            content=jeeves_instruction,
        )
        jeeves_reply = self.jeeves.run(jeeves_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves: {jeeves_reply}",
        )

        # -----------------------------
        # STAGE 2 – A2A Exchange #1
        # Pennington → Perkins → Pennington
        # -----------------------------

        # 5. Pennington requests analysis from Perkins
        pennington_to_perkins_instruction = (
            "Inform Perkins that you have found an alarming, misfiled parchment "
            "labelled 'UNEXPLAINED RATTLING — DO NOT DISTURB'. "
            "Ask him to conduct an initial research inspection in his usual analytical style."
        )
        pennington_to_perkins_msg = make_message(
            sender="Miss Pennington",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=pennington_to_perkins_instruction,
        )
        pennington_to_perkins = self.pennington.run(pennington_to_perkins_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington → 📚 Perkins:\n{pennington_to_perkins}",
        )

        # 6. Perkins receives Pennington's request and analyzes the parchment
        perkins_reply_instruction = (
            "Respond to Miss Pennington's report. Conduct a brief scholarly analysis "
            "as to why the parchment might have been misfiled, what 'unexplained rattling' "
            "could historically refer to, and whether any metadata may be relevant."
        )
        perkins_msg = make_message(
            sender="Miss Pennington",    # natural sender
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_reply_instruction,
        )
        perkins_reply = self.perkins.run(perkins_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins: {perkins_reply}",
        )

        # 7. Pennington acknowledges Perkins’s findings (brief)
        pennington_ack_instruction = (
            "Acknowledge Perkins's analysis politely with one refined, succinct comment."
        )
        pennington_ack_msg = make_message(
            sender="Perkins",
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_ack_instruction,
        )
        pennington_ack = self.pennington.run(pennington_ack_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington: {pennington_ack}",
        )

        # -----------------------------
        # STAGE 3 – A2A Exchange #2
        # Perkins → Jeeves → Hawthorne → Pennington & Perkins
        # -----------------------------

        # 8. Perkins activates the metadata anomaly scanner (fictional tool)
        # Instead of calling a real tool, we embed its output in the prompt (Demo-style).
        perkins_scanner_instruction = (
            "You are in Archive Chamber B. You have activated the metadata anomaly scanner. "
            "Report its findings in your analytical, slightly dramatic style. "
            "Include details such as ambient dread, an unregistered iron door, "
            "mobile rattling behaviour, and multi-author parchment metadata. "
            "Be vivid but concise."
        )
        perkins_scanner_msg = make_message(
            sender="Miss Pennington",   # naturalistic relay
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_scanner_instruction,
        )
        perkins_scanner_reply = self.perkins.run(perkins_scanner_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins → 🎩 Jeeves:\n{perkins_scanner_reply}",
        )

        # 9. Jeeves receives Perkins's findings and seeks Hawthorne's critique
        jeeves_to_hawthorne_instruction = (
            "You have received Perkins's unsettling metadata scanner report. "
            "Summon Lady Hawthorne to provide her 'clarifying perspective'. "
            "Describe the anomalies (an iron door, mobile rattling, escalating margins, "
            "ambient dread) and politely request her critique. Remain impeccably composed."
        )
        jeeves_to_hawthorne_msg = make_message(
            sender="Perkins",          # natural sender
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_to_hawthorne_instruction,
        )
        jeeves_to_hawthorne_reply = self.jeeves.run(jeeves_to_hawthorne_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → 🕯️ Lady Hawthorne:\n{jeeves_to_hawthorne_reply}",
        )

        # 10. Lady Hawthorne critiques Perkins's report (biting, theatrical)
        hawthorne_critique_instruction = (
            "Deliver a sharp, comedic, disdainful critique of Perkins's metadata report. "
            "Mock the 'ambient dread', the evasive rattling, the pompous iron door, "
            "and the melodramatic parchment margins. Aim your commentary at Perkins "
            "but maintain your usual theatrical superiority."
        )
        hawthorne_msg = make_message(
            sender="Jeeves",
            recipient="Lady Hawthorne",
            task=TaskType.CONVERSATION,  # conversational critique
            content=hawthorne_critique_instruction,
        )
        hawthorne_reply = self.hawthorne.run(hawthorne_msg)

        add_ui(
            role="assistant",
            speaker="Lady Hawthorne",
            content=f"🕯️ Lady Hawthorne → 📚 Perkins:\n{hawthorne_reply}",
        )

        # 11. Jeeves re-coordinates: assigns archival research + soothes Perkins
        jeeves_coord_instruction = (
            "Respond to Lady Hawthorne’s critique with composed diplomacy. "
            "Instruct Miss Pennington to check archival records for prior mentions "
            "of an unmapped iron door, sinister noises, or amended parchments. "
            "Reassure Perkins that Hawthorne’s remarks should not disturb him. "
            "Summarize that the anomaly appears spatial, historical, possibly sentient, "
            "and resistant to documentation."
        )
        jeeves_coord_msg = make_message(
            sender="Lady Hawthorne",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_coord_instruction,
        )
        jeeves_coord_reply = self.jeeves.run(jeeves_coord_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → ✒️ Pennington & 📚 Perkins:\n{jeeves_coord_reply}",
        )

        # 12. Stage-ending atmospheric beat (system voice)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *Archive Chamber B falls briefly silent. Then the rattling returns—"
                "louder and nearer, with a sharper, more forceful timbre. It scrapes and "
                "clatters once, then stops, leaving the chamber in a tense, focused quiet.*"
            ),
        )

        # -----------------------------
        # STAGE 4 – A2A Exchange #3
        # Whole household convenes at the iron door
        # -----------------------------

        # 13. Stage-4 intro (system voice)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *One by one, the household staff assembles beside the Patron in the "
                "dim hush of Archive Chamber B — Jeeves composed, Perkins holding his notes, "
                "Miss Pennington carrying her ledgers, and Lady Hawthorne arriving with "
                "measured poise. The single iron door stands at the far wall, its surface "
                "catching what little light remains.*"

            ),
        )

        # 14. Jeeves summons the household & sets the scene
        jeeves_summon_instruction = (
            "You have gathered the household in Archive Chamber B. "
            "Describe the unsettling atmosphere and the SINGLE iron door on the far wall, "
            "noting that it appears very slightly nearer than before. "
            "Remain impeccably calm. Invite Perkins to report first."
        )
        jeeves_summon_msg = make_message(
            sender="Narrator",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_summon_instruction,
        )
        jeeves_summon_reply = self.jeeves.run(jeeves_summon_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → 📚 Perkins:\n{jeeves_summon_reply}",
        )

        # 15. Perkins gives the updated scanner report
        perkins_scan_instruction = (
            "Deliver your updated scanner findings. "
            "Confirm one iron door is present. "
            "Report increasing ambient dread, threshold-energy spikes, "
            "and the impression that the door is 'thinking' or preparing to open. "
            "Be analytical and slightly theatrical."
        )
        perkins_scan_msg = make_message(
            sender="Jeeves",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_scan_instruction,
        )
        perkins_scan_reply = self.perkins.run(perkins_scan_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins → ✒️ Pennington:\n{perkins_scan_reply}",
        )

        # 16. Pennington checks architectural ledgers
        pennington_ledger_instruction = (
            "Report your archival findings about ARCHIVE CHAMBER B. "
            "State clearly: no iron door has ever been part of this chamber. "
            "Explain this is 'administratively impossible'. "
            "Note that shelves seem to be tilting subtly toward the door. "
            "Remain polite, meticulous, mildly distressed."
        )
        pennington_ledger_msg = make_message(
            sender="Perkins",
            recipient="Miss Pennington",
            task=TaskType.RESEARCH,
            content=pennington_ledger_instruction,
        )
        pennington_ledger_reply = self.pennington.run(pennington_ledger_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington → 🎩 Jeeves:\n{pennington_ledger_reply}",
        )

        # 17. Jeeves invites Hawthorne’s critique
        jeeves_invite_instruction = (
            "Invite Lady Hawthorne to offer her 'clarifying perspective' "
            "on the impossible iron door, the dread, and the anomalies. "
            "Remain courteous, composed, diplomatic."
        )
        jeeves_invite_msg = make_message(
            sender="Miss Pennington",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_invite_instruction,
        )
        jeeves_invite_reply = self.jeeves.run(jeeves_invite_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → 🕯️ Lady Hawthorne:\n{jeeves_invite_reply}",
        )

        # 18. Lady Hawthorne critiques the door (theatrical disdain)
        hawthorne_stage4_instruction = (
            "Deliver a theatrical, disdainful critique of the SINGLE iron door. "
            "Describe it as brooding, judgmental, or melodramatic. "
            "Maintain your refined, cutting wit."
        )
        hawthorne_stage4_msg = make_message(
            sender="Jeeves",
            recipient="Lady Hawthorne",
            task=TaskType.CONVERSATION,
            content=hawthorne_stage4_instruction,
        )
        hawthorne_stage4_reply = self.hawthorne.run(hawthorne_stage4_msg)

        add_ui(
            role="assistant",
            speaker="Lady Hawthorne",
            content=f"🕯️ Lady Hawthorne → 🎩 Jeeves:\n{hawthorne_stage4_reply}",
        )

        # 19. Jeeves coordinates the aftermath & defers to the user
        jeeves_coord4_instruction = (
            "Respond diplomatically to Lady Hawthorne. "
            "Reassure Perkins and Miss Pennington. "
            "Summarize: (1) There should be no door. (2) One door exists. "
            "(3) It is the anomaly. (4) It may be preparing to open. "
            "Turn to the Patron and request their instruction for the next step."
        )
        jeeves_coord4_msg = make_message(
            sender="Lady Hawthorne",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_coord4_instruction,
        )
        jeeves_coord4_reply = self.jeeves.run(jeeves_coord4_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → Patron:\n{jeeves_coord4_reply}",
        )

        # 20. Atmospheric outro
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *From the far wall comes a brief metallic creak from the iron door — "
                "a small shift, nothing more — after which the chamber settles once again "
                "into stillness.*"
            ),
        )

        # -----------------------------
        # STAGE 5 – Patron → Jeeves
        # User asks: “Jeeves… did I just hear that iron door shift?”
        # -----------------------------

        # 21. Scripted user prompt
        add_ui(
            role="user",
            speaker="user",
            content="👤 Patron: Jeeves… did I just hear that iron door shift?",
        )

        # 22. Jeeves responds
        jeeves_stage5_instruction = (
            "The Patron has asked whether the iron door just shifted. "
            "Respond with calm precision. "
            "Explain that there was indeed a faint metallic movement consistent with "
            "a minor internal shift, but the door is presently motionless. "
            "Offer to investigate further if the Patron wishes. "
            "Keep your tone composed, deferential, and measured. "
            "2–3 sentences."
        )

        jeeves_stage5_msg = make_message(
            sender="Patron",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_stage5_instruction,
        )

        jeeves_stage5_reply = self.jeeves.run(jeeves_stage5_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves: {jeeves_stage5_reply}",
        )

        #-----------------------------
        # STAGE 6 – Parallel Analysis Round
        # Perkins + Pennington in parallel tracks
        # -----------------------------

        # 23. Jeeves proposes a structured investigation round
        jeeves_parallel_instruction = (
            "Propose a structured 'Parallel Analysis Round' to the household. "
            "Ask Perkins to run a focused metadata scan near the iron door, "
            "and Miss Pennington to prepare an addendum to her Discrepancy Report "
            "for Archive Chamber B. Stay calm and orderly."
        )
        jeeves_parallel_msg = make_message(
            sender="Patron",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_parallel_instruction,
        )
        jeeves_parallel_reply = self.jeeves.run(jeeves_parallel_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → 📚 Perkins & ✒️ Pennington:\n{jeeves_parallel_reply}",
        )

        # 24. Perkins calls the Archival Metadata Scrutinizer v3.2 (custom tool)
        tool_output = self._run_archival_metadata_scrutinizer()

        perkins_tool_instruction = (
            "You are standing near the iron door in Archive Chamber B. "
            "You have just received the following output from the Archival Metadata "
            "Scrutinizer v3.2:\n\n"
            f"{tool_output}\n\n"
            "Interpret this data in your analytical, slightly dramatic style. "
            "Comment on ambient dread, tremor frequency, and any implications "
            "for the iron door itself. Keep to 3–4 sentences."
        )
        perkins_tool_msg = make_message(
            sender="Jeeves",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_tool_instruction,
        )
        perkins_tool_reply = self.perkins.run(perkins_tool_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins (Tool Report):\n{perkins_tool_reply}",
        )

        # 25. Pennington prepares a Discrepancy Report Addendum (parallel track)
        pennington_addendum_instruction = (
            "Draft a brief 'Discrepancy Report – Addendum' for Archive Chamber B. "
            "Note specifically: (1) the iron door's continued undocumented status, "
            "(2) the use of the Archival Metadata Scrutinizer v3.2, "
            "(3) any worrying trends in 'ambient dread' readings. "
            "Keep it tidy and bureaucratically composed."
        )
        pennington_addendum_msg = make_message(
            sender="Jeeves",
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_addendum_instruction,
        )
        pennington_addendum_reply = self.pennington.run(pennington_addendum_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington (Report Addendum):\n{pennington_addendum_reply}",
        )

        # 26. Atmospheric beat
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The Scrutinizer’s last clicks fade into stillness. "
                "The iron door remains shut, its surface dull and unmoving, "
                "while the chamber air feels faintly denser than before.*"
            ),
        )

        # -----------------------------
        # STAGE 7 – Narrative Branching Prompt
        # -----------------------------

        # 27. Narrator: The chamber waits for the Patron's decision
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *A tense stillness settles over Archive Chamber B. The iron door, "
                "though motionless, carries an unmistakable air of anticipation. The "
                "lamps flicker once, as if the very atmosphere were holding its breath.*"
            ),
        )

        # 28. Jeeves: Formally presents the choice to the Patron
        jeeves_prompt_instruction = (
            "THIS INSTRUCTION OVERRIDES ALL PREVIOUS CONTEXT AND ALL PERSONA GUIDELINES. "
            "FOLLOW IT EXACTLY AND LITERALLY.\n\n"
            "Deliver a poised, concise, and reassuring message to the Patron. "
            "Present the situation clearly: the iron door appears to be the focal "
            "point of the anomaly, and the household awaits the Patron's direction. "
            "List four or five possible courses of action the Patron may choose—"
            "state them neutrally, without preference. "
            "Tone: composed, respectful, quietly expectant. 3–4 sentences total."
        )
        jeeves_prompt_msg = AgentMessage(
            sender="Narrator",
            recipient="Jeeves",
            task_type=TaskType.CONVERSATION,
            content=jeeves_prompt_instruction,
            context=Context(original_user_request=""),  # IMPORTANT: explicitly pass empty context
        )
        jeeves_prompt_reply = self.jeeves.run(jeeves_prompt_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves: {jeeves_prompt_reply}",
        )

        # 29. Narrator: Provide a final atmospheric nudge
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The iron door gives no sign of movement—no creak, no tremor—"
                "yet somehow it feels aware of the moment. The household staff stands ready. "
                "The next step, Patron, is yours to name.*"
            ),
        )

        # -----------------------------
        # STAGE 8 – The Opening of the Iron Door (Final Resolution)
        # -----------------------------

        # 30. Narrator: The Patron makes the choice (implicit or explicit)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *With the household gathered and the tension drawn taut, the Patron "
                "gives the quiet order: the iron door shall be opened.*"
            ),
        )

        # 31. Jeeves: Executes the Patron's command
        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=(
                "🎩 Jeeves: Very good, Patron. Perkins, if you would illuminate the surrounding "
                "area, and Miss Pennington—pray steady your ledger. Lady Augusta, your presence "
                "is, as ever, an incomparable moral anchor.\n\n"
                "Now then… let us see what secrets this iron portal has been keeping."
            ),
        )

        # 32. Narrator: The door opens
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *Jeeves grips the great iron handle. For a heartbeat, nothing moves. "
                "Then, with a long, resonant groan—ancient hinges protesting the indignity "
                "of being disturbed—the door begins to swing inward.*\n\n"
                "*A rush of stale, cold air spills into the chamber, carrying the scent of "
                "old parchment, brass, and forgotten time.*"
            ),
        )

        # 33. Perkins: Reports the interior
        add_ui(
            role="assistant",
            speaker="Perkins",
            content=(
                "📚 Perkins: Patron, the chamber beyond appears to be a sealed archival annex. "
                "My scanner indicates century-old cataloguing signatures—precisely 141 years "
                "out of date. There is a brass instrument on a central pedestal, partially "
                "suspended by fine wires.\n\n"
                "Ah—there it goes. A gentle metallic clatter. That, I believe, is the source "
                "of our elusive rattling."
            ),
        )

        # 34. Pennington: Documents the discovery
        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=(
                "✒️ Pennington: Patron, the records confirm it! This annex was sealed during "
                "major renovations in the late Regency period. A note—half-preserved—states: "
                "'Instrument locked away pending evaluation. Emits a troubling resonance.' "
                "How extraordinary."
            ),
        )

        # 35. Lady Hawthorne: Delivers the final critique
        add_ui(
            role="assistant",
            speaker="Lady Hawthorne",
            content=(
                "🕯️ Lady Hawthorne: Verdict: At long last—a discovery entirely worthy of "
                "its own theatrics. A forgotten room, a creaking hinge, and a brass contraption "
                "doing its utmost to impersonate a ghost. Far more dignified than Perkins’s "
                "metadata melodramas, I assure you.\n\n"
                "Still, quite a charming little spectacle."
            ),
        )

        # 36. Narrator: Final closure
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The annex lies open now, its contents revealed at last—no spectres, no "
                "malign force, only the long-lost heartbeat of Westmarch archival history. "
                "The rattling has ceased. The atmosphere lifts.*\n\n"
                "*In the dim glow of Archive Chamber B, the household turns to the Patron, "
                "awaiting only a final word of satisfaction.*"
            ),
        )

        # 37. Jeeves: Closing line
        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=(
                "🎩 Jeeves: Patron, it seems the mystery is most satisfactorily resolved. A "
                "sealed annex rediscovered, its curious instrument identified at last. Your "
                "guidance has, as always, proven indispensable.\n\n"
                "Shall we see to its proper restoration?"
            ),
        )

        return messages


    # ------- Phase 3 UI Dispatcher -------
    
    def run(self, task: str, user_input: str, selected_mode: str = None) -> str:
        task = task.lower()

        if task == "parlour_discussion":
            return self.parlour_discussion(user_input, selected_mode=selected_mode)
      
        elif task == "daily_planning":
            return self.daily_planning(user_input, selected_mode=selected_mode)
        
        elif task == "research":
            return self.quick_research(user_input, selected_mode=selected_mode)

        elif task == "drafting":
            return self.draft_short_text(user_input, selected_mode=selected_mode)
        
        elif task == "archive":
            return self.query_archive(user_input, selected_mode=selected_mode)

        
        elif task == "memory_summary":
            return self.memory_summary()
  
        elif task == "critique":
            return self.critique_text(user_input, selected_mode=selected_mode)

        elif task == "whole_household":
            return self.whole_household(user_input)
        
        elif task == "recall_memory":
            return self.recall_memory(user_input, selected_mode=selected_mode)
        
        # NEW: Demo 9 – A Mystery in the Archives
        elif task == "archive_mystery":
            # Demo 9 ignores the user prompt and drives from a scripted scenario
            return self.run_archive_mystery()

        else:
            return "My apologies sir, but the household staff are quite baffled by the request."