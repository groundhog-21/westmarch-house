# westmarch/orchestrator/router.py

from __future__ import annotations
from westmarch.core.messages import TaskType


def classify_task(user_input: str) -> TaskType:
    text = user_input.lower()

    # Conversational cues
    if any(phrase in text for phrase in [
        "jeeves", 
        "old chap",
        "my good man",
        "my dear fellow",
        "hello",
        "hi there",
        "good morning",
        "good evening",
        "let us discuss",
        "i wonder",
        "i say",
    ]):
        return TaskType.CONVERSATION

    # Planning cues
    if "plan my day" in text or "schedule" in text:
        return TaskType.PLANNING

    # Research cues
    if any(word in text for word in ["research", "difference", "compare", "investigate"]):
        return TaskType.RESEARCH

    # Drafting cues
    if any(word in text for word in ["email", "rewrite", "draft", "compose"]):
        return TaskType.DRAFTING

    # Critique cues
    if any(word in text for word in ["critique", "review", "opinion on", "how does this read"]):
        return TaskType.CRITIQUE

    # Multi-step tasks (Jeeves + Perkins + Pennington + possibly Hawthorne)
    if any(word in text for word in ["project", "trip", "itinerary", "plan a trip"]):
        return TaskType.MIXED

    return TaskType.UNKNOWN