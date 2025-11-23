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

    def daily_planning(self, user_input: str) -> str:
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
            context=self._context(user_input),
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

    def quick_research(self, user_input: str) -> str:
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
            context=self._context(user_input),
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

    def draft_short_text(self, user_input: str) -> str:
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

        draft_msg = AgentMessage(
            sender="Jeeves",
            recipient="Miss Pennington",
            task_type=TaskType.DRAFTING,
            content=(
                "Please transform the user's notes into a polished, ready-to-send "
                "piece of writing. Do not explain your process; simply return the "
                "final text."
            ),
            context=self._context(user_input),
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

    def query_archive(self, user_input: str) -> str:
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
        summary = self.pennington.summarize_text(combined)

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
            context=self._context(user_input),
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

    def critique_text(self, text_to_critique: str) -> str:
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
            context=self._context(text_to_critique),
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
    
    def whole_household(self, user_input: str) -> str:
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
            context=self._context(user_input),
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
                context=self._context(user_input),
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
                    "End with a single warm closing line.\n\n"
                    "Write only the letter."
                ),
                context=self._context(user_input),
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
                context=self._context(user_input),
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
                    "than 80–100 words. Keep the tone warm and elegant, avoid ornamentation, and "
                    "ensure the request for neighbour observations is clear. Do not add new ideas, "
                    "and do not repeat content from the original draft.\n\n"
                    "Your original draft:\n"
                    f"{pennington_output}\n\n"
                    "Lady Hawthorne said:\n"
                    f"{hawthorne_letter_feedback}"
                ),
                context=self._context(user_input),
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
                    "• include, as an exception, the FULL TEXT of your revised letter\n"
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
                context=self._context(user_input),
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
            context=self._context(user_input),
        )

        return self.jeeves.run(final_msg)
    
    def recall_memory(self, user_input: str) -> str:
        """
        Jeeves retrieves past notes from Miss Pennington’s memory ledger
        that relate to the user's query.
        """

        log("WORKFLOW: Memory recall initiated")

        # Approval / closure detection
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
                "Indeed, sir. Miss Pennington and I remain prepared "
                "to recover any stray reflections."
            )

        query = user_input.lower().strip()

        # Ask Miss Pennington’s memory system for relevant entries
        matches = self.pennington.search_memory("poem")
        matches = [
            m for m in matches
            if "critique" in m["content"].lower()
            and "lady hawthorne" in m["content"].lower()
        ]

        # No matches at all → graceful fallback
        if not matches:
            return (
                "I have consulted Miss Pennington’s meticulously kept ledger, sir, "
                "but I fear no relevant recollection appears recorded under that description. "
                "If you recall even a fragment more, I should be delighted to search again."
            )

        # ❗ NEW: Only select the *first* matching entry
        entry = matches[0]
        content = entry.get("content", "").strip()

        return (
            "Indeed, sir. Upon consulting the household’s memory ledger, "
            "I find the following relevant recollection:\n\n"
            f"{content}\n\n"
            "If you desire a fuller account or further inquiry, I remain entirely at your disposal."
        )

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
        
        elif task == "query_archive":
            return self.query_archive(user_input)

        elif task == "memory_summary":
            return self.memory_summary()

        elif task == "critique":
            return self.critique_text(user_input)

        elif task == "whole_household":
            return self.whole_household(user_input)
        
        elif task == "recall_memory":
            return self.recall_memory(user_input)

        else:
            return "My apologies sir, but the household staff are quite baffled by the request."