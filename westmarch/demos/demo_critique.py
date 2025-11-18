# westmarch/demos/demo_critique.py

"""
Demo: Lady Hawthorne’s Critique Workflow
This script tests the refined critique workflow using:
- Direct patron input
- Perkins’ research report
- Miss Pennington’s draft
- A snippet from a planning workflow

Run with:
    python demo_critique.py
"""

from westmarch.orchestrator.workflows import WestmarchOrchestrator
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.core.models import ModelClient


def build_orchestrator():
    """Replicates the exact construction used by other Phase-2 demos."""
    jeeves = JeevesAgent(ModelClient("jeeves"))
    perkins = PerkinsAgent(ModelClient("perkins"))
    pennington = MissPenningtonAgent(ModelClient("miss_pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient("lady_hawthorne"))
    return WestmarchOrchestrator(jeeves, perkins, pennington, hawthorne)


def header(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def run_demo():
    orch = build_orchestrator()

    # ---------------------------------------------------
    # 1. Direct patron critique
    # ---------------------------------------------------
    header("TEST 1 — Patron Text Critique")
    text = "The garden party was fun and everyone liked it."
    result = orch.critique_text(text)
    print(result)

    # ---------------------------------------------------
    # 2. Critique of Perkins' research report
    # ---------------------------------------------------
    header("TEST 2 — Critiquing Perkins’ Research Report")
    perkins_report = (
        "Perkins’ Findings: Tea consumption increased 12% compared to last quarter."
    )
    result = orch.critique_text(perkins_report)
    print(result)

    # ---------------------------------------------------
    # 3. Critique of Miss Pennington’s draft
    # ---------------------------------------------------
    header("TEST 3 — Critiquing Miss Pennington’s Draft")
    pennington_draft = (
        "Miss Pennington's Draft: A brief note expressing gratitude for attendance."
    )
    result = orch.critique_text(pennington_draft)
    print(result)

    # ---------------------------------------------------
    # 4. Critique of output from a planning workflow
    # ---------------------------------------------------
    header("TEST 4 — Critiquing Jeeves’ Structured Plan")
    sample_plan = (
        "1. Breakfast at 8:00. 2. Emails until 10:00. 3. Gym at noon. "
        "4. Afternoon meeting with the estate accountant."
    )
    result = orch.critique_text(sample_plan)
    print(result)

    # ---------------------------------------------------
    # 5. Recursion Prevention Check
    # ---------------------------------------------------
    header("TEST 5 — Recursion & Meta-Critique Prevention")

    tricky = "Please critique the following critique: It is overly long."
    result = orch.critique_text(tricky)      # <-- DO NOT lower-case!

    # We create a lowercase copy ONLY for forbidden-pattern checking
    result_lower = result.lower()

    forbidden = [
        "your critique above",
        "the earlier critique",
        "my critique above",
        "in my previous critique",
    ]

    # Direct-detection of Lady Hawthorne critiquing a critique explicitly
    if result_lower.startswith("indeed, sir. i have reviewed lady hawthorne"):
        print("[WARNING] Hawthorne is critiquing a critique directly.")

    # Forbidden phrases meaning recursion or self-referential critique
    if any(bad in result_lower for bad in forbidden):
        print("[WARNING] Recursion or self-referential critique detected:\n")

    print(result)


if __name__ == "__main__":
    run_demo()