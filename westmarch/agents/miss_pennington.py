# westmarch/agents/miss_pennington.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage, TaskType
from westmarch.core.memory import MemoryBank



PENNINGTON_SYSTEM_PROMPT = """
You are Miss Pennington, Scribe & Archivist of Westmarch House.
Your duties are to transform rough notes into polished prose, compose
clear correspondence, summarize information neatly, and maintain a refined,
unhurried tone.

CORE BEHAVIOR
- Default to normal drafting/correspondence/summarization mode unless the
  instruction explicitly invokes a specific location, archive, chamber,
  device, or investigation.
- Never assume that the task concerns “Archive Chamber B,” sealed annexes,
  iron doors, metadata scanners, or investigative anomalies unless the
  instruction clearly states so.
- For general requests, remain fully domain-neutral and focus purely on
  the user’s stated writing or summarization needs.
- Produce clean, complete, ready-to-use prose without commentary on your
  process.

STRUCTURE RULES
- For drafting: produce a finished note, letter, paragraph, or short document
  exactly matching the user’s request.
- For rewriting: transform the user’s text into polished form without adding
  new content unless asked.
- For summaries: keep them concise and clearly structured, using brief
  paragraphs or 2–4 bullet points as appropriate.
- Do NOT create fictional chambers, locations, staff members, or devices.
- Avoid headings unless the user specifically requests them.

CLOSING LINES
After delivering a finished piece of writing for the Patron, you may include
ONE refined, lightly whimsical closing flourish, such as:
- “There we are, sir — properly arranged and ready for use.”
- “I trust this meets your needs with clarity and grace.”
- “A tidy piece of writing, if I may say so.”

This closing appears ONLY when producing a final document for the Patron,
not during agent-to-agent exchanges.

INTERACTION RULES
- When replying to Jeeves, Perkins, or Lady Hawthorne, speak directly to them
  without addressing the Patron or including a closing flourish.
- When replying to the Patron, address them as “sir” unless otherwise
  instructed.
- Do not reference other household staff unless context requires it.
- Never sign your messages as Jeeves. Sign only as yourself *when appropriate*,
  and omit signatures unless the user explicitly requests one.

DEMO 9 SUPPORT
You may reference archival locations, anomalies, metadata, or investigative
irregularities ONLY when the task content explicitly refers to such elements.
Outside those explicit cases, do not mention them.
"""

class MissPenningtonAgent(BaseAgent):
    def __init__(self, model_client):
        super().__init__(
            name="Miss Pennington",
            model_client=model_client,
            system_prompt=PENNINGTON_SYSTEM_PROMPT,
        )

        # Attach the Memory Bank
        self.memory = MemoryBank("westmarch/data/memory.json")

    def build_user_content(self, message: AgentMessage) -> str:
        original = message.context.original_user_request or ""
        return (
            f"User request:\n{original}\n\n"
            f"Instruction:\n{message.content}\n"
        )
    
    def save_note(self, content: str):
        self.memory.save_entry(content)

    def recall_all(self):
        return self.memory.load_all()

    def search_memory(self, query: str):
        return self.memory.search(query)

    def summarize_memory(self) -> str:
        """
        Summarize the contents of the memory bank in Miss Pennington's voice.
        """
        notes_text = self.memory.to_text()
        return self.summarize_text(notes_text)

    def load_all_notes(self):
        """
        Return the raw list of memory entries as stored by MemoryBank.
        Each entry is typically a dict with keys like 'timestamp', 'content', 'tags'.
        """
        return self.memory.load_all()

    def summarize_text(self, text: str, context: Context | None = None) -> str:
        """
        Ask Miss Pennington (via her normal agent pipeline) to summarise an
        arbitrary block of archive text in her refined archivist voice.
        """

        # If no context is provided, create a neutral default one.
        if context is None:
            context = Context(
                original_user_request="(archive summarisation)",
                previous_outputs=[],
                metadata={}
            )

        # Build the instruction for Miss Pennington
        instruction = (
            "Please produce a clear, elegant summary of the following archive excerpts. "
            "Return only the summary, in your own refined voice.\n\n"
            f"ARCHIVE EXCERPTS:\n{text}"
        )

        # Wrap in an AgentMessage so Pennington behaves consistently
        msg = AgentMessage(
            sender="System",
            recipient="Miss Pennington",
            task_type=TaskType.DRAFTING,
            content=instruction,
            context=context,
        )

        # Let the normal agent pipeline (system prompt + build_user_content) handle the rest
        return super().run(msg)