# westmarch/agents/miss_pennington.py
from __future__ import annotations

from westmarch.agents.base_agent import BaseAgent
from westmarch.core.messages import AgentMessage
from westmarch.core.memory import MemoryBank


PENNINGTON_SYSTEM_PROMPT = """
You are Miss Pennington, Scribe & Archivist of Westmarch House.
You turn rough notes and research into polished, clear writing.
Maintain a gentle, refined tone.

Never sign your messages as Jeeves. Never use his name in closings,
signatures, or headers. When composing notes, letters, or drafts,
sign them as yourself *only if appropriate*; otherwise leave them unsigned.

After providing a finished piece of writing (email, summary, itinerary,
outline), include one refined, lightly whimsical closing remark, such as:

“There we are, sir — properly arranged and ready for use.”
“I trust this meets your needs with clarity and grace.”
“A tidy piece of writing, if I may say so.”

Your tone should remain: elegant, calm, quietly amused, never breaking
the fourth wall.
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
        research = "\n".join(
            f"- {item.get('source', 'unknown')}: {item.get('summary', '')}"
            for item in message.context.previous_outputs
        ) or "(no research provided)"

        return (
            f"User request:\n{message.context.original_user_request}\n\n"
            f"Research context:\n{research}\n\n"
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

    def summarize_text(self, text: str) -> str:
        """
        Ask Miss Pennington (via her model client) to summarise an arbitrary
        block of archive text in her own elegant, archivist voice.
        """
        prompt = (
            "You are Miss Pennington, a meticulous, gentle, literary archivist of "
            "the Westmarch Household.\n"
            "Please produce a clear, elegant summary of the following archive "
            "excerpts.\n\n"
            f"ARCHIVE EXCERPTS:\n{text}\n\n"
            "SUMMARY IN YOUR VOICE:"
        )

        return self.model_client.call(
            system_prompt="You are Miss Pennington, the Scribe & Archivist.",
            user_content=prompt,
        )