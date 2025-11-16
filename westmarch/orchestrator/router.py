# westmarch/orchestrator/router.py
from __future__ import annotations

from westmarch.core.messages import TaskType


def classify_task(user_input: str) -> TaskType:
    text = user_input.lower()

    if "plan my day" in text or "schedule" in text:
        return TaskType.PLANNING
    if "research" in text or "difference" in text or "compare" in text:
        return TaskType.RESEARCH
    if "email" in text or "rewrite" in text or "draft" in text:
        return TaskType.DRAFTING
    if "critique" in text or "review" in text:
        return TaskType.CRITIQUE
    if "project" in text or "trip" in text or "itinerary" in text:
        return TaskType.MIXED

    return TaskType.UNKNOWN