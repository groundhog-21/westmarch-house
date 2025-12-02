# westmarch/core/tagging.py
from __future__ import annotations

from typing import List, Optional, Set


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
        "critique", "appraisal", "assessment"
    ],

    # Sports (new domain per your instruction)
    "sports": [
        "sport", "sports", "tennis", "match", "tournament",
        "score", "set", "athlete", "competition"
    ]
}

def infer_domains(text: str) -> set[str]:
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

    for domain, keywords in DOMAIN_KEYWORDS.items():
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

def infer_tags_from_user_input(user_input: str | None) -> list[str]:
    """
    Infer domain tags from the user_input text.
    Returns domain:* tags such as ["domain:poetry", "domain:gnome"].
    Returns [] if nothing found.
    """
    if not user_input or not user_input.strip():
        return []

    domains = infer_domains(user_input)
    tags = [f"domain:{d}" for d in sorted(domains)]
    return tags
