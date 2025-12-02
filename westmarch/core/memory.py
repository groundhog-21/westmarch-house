# westmarch/core/memory.py
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

from westmarch.core.logging import log


class MemoryBank:
    """
    A simple persistent JSON-based memory store for Miss Pennington.
    Stores entries with timestamp, content, and optional tags.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Ensure file exists
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load(self) -> List[Dict]:
        log("MEMORY: Loading all notes")  # <<< ADDED

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                log(f"MEMORY: Loaded {len(data)} notes")  # <<< ADDED
                return data
        except json.JSONDecodeError:
            log("MEMORY: JSON decode error — returning empty list")  # <<< ADDED
            return []

    def _save(self, data: List[Dict]):
        log(f"MEMORY: Saving file with {len(data)} entries")  # <<< ADDED
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log("MEMORY: Save complete")  # <<< ADDED

    def save_entry(self, content: str, tags: Optional[List[str]] = None):
        log(f"MEMORY: Saving note ({len(content.split())} words)")

        # ---------- AUTO-TAGGING ----------
        auto_tags = ["auto"]

        lower = content.lower()

        import re

        # 1. Type classification based on workflow prefixes.
        if lower.startswith("parlour discussion entry"):
            type_tag = "type:parlour"

        elif lower.startswith("daily plan created"):
            type_tag = "type:daily-plan"

        elif lower.startswith("daily plan finalized"):
            type_tag = "type:daily-plan"

        elif lower.startswith("research performed"):
            type_tag = "type:research"

        elif lower.startswith("drafted text based"):
            type_tag = "type:draft"

        elif lower.startswith("critique requested"):
            type_tag = "type:critique"

        elif lower.startswith("[whole household]"):
            type_tag = "type:investigation"

        # 2. Historical / archival material (contains years 1000–1999)
        elif re.search(r"\b(1[0-9]{3})\b", content):
            type_tag = "type:archive"

        else:
            type_tag = "type:note"

        auto_tags.append(type_tag)

        # 3. Domain inference (safe and robust)
        try:
            from westmarch.orchestrator.workflows import WestmarchOrchestrator
            domains = list(WestmarchOrchestrator.infer_domains(content))
            domain_tags = [f"domain:{d}" for d in domains]
        except Exception:
            domain_tags = []

        # 4. Merge tags: auto → domain → manual
        final_tags = auto_tags + domain_tags + (tags or [])
        # ------------------------------------

        data = self._load()

        # Normalise and deduplicate tags while preserving order
        unique_tags = []
        if tags:
            seen = set()
            for t in tags:
                if t not in seen:
                    unique_tags.append(t)
                    seen.add(t)

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "content": content.strip(),
            "tags": unique_tags,
        }

        data.append(entry)
        self._save(data)

        log("MEMORY: Note saved successfully")

    def load_all(self) -> List[Dict]:
        return self._load()

    def search(self, query: str) -> List[Dict]:
        log(f"MEMORY: Searching for '{query}'")  # <<< ADDED
        q = query.lower()

        data = self._load()
        results = [
            e for e in data
            if q in e["content"].lower()
            or any(q in tag.lower() for tag in e["tags"])
        ]

        log(f"MEMORY: Found {len(results)} matching entries")  # <<< ADDED
        return results

    def to_text(self) -> str:
        log("MEMORY: Converting memory entries to text")  # <<< ADDED

        entries = self._load()
        if not entries:
            log("MEMORY: No entries to convert")  # <<< ADDED
            return "No memory entries available."

        lines = []
        for e in entries:
            ts = e.get("timestamp", "")
            content = e.get("content", "")
            tags = ", ".join(e.get("tags", [])) if e.get("tags") else "none"
            lines.append(f"- [{ts}] ({tags}) {content}")

        log(f"MEMORY: Prepared text for {len(entries)} entries")  # <<< ADDED
        return "\n".join(lines)