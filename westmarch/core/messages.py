# westmarch/core/messages.py
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class TaskType(str, Enum):
    PLANNING = "planning"
    RESEARCH = "research"
    DRAFTING = "drafting"
    CRITIQUE = "critique"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class Constraints:
    length_limit: str = "medium"
    style: str = "neutral"
    special_instructions: str = ""


@dataclass
class Context:
    original_user_request: str
    previous_outputs: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    task_type: TaskType
    content: str
    context: Context
    constraints: Constraints = field(default_factory=Constraints)