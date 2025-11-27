# westmarch/demos/test_full_pipeline.py

from westmarch.core.models import ModelClient
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.orchestrator.workflows import WestmarchOrchestrator


def build_orchestrator():
    """
    Local construction of all agents and the orchestrator.
    This matches your current project structure.
    """
    jeeves_client = ModelClient("Jeeves")
    perkins_client = ModelClient("Perkins")
    pennington_client = ModelClient("Miss Pennington")
    hawthorne_client = ModelClient("Lady_Hawthorne")

    jeeves = JeevesAgent(jeeves_client)
    perkins = PerkinsAgent(perkins_client)
    pennington = MissPenningtonAgent(pennington_client)
    hawthorne = LadyHawthorneAgent(hawthorne_client)

    return WestmarchOrchestrator(
        jeeves=jeeves,
        perkins=perkins,
        pennington=pennington,
        hawthorne=hawthorne,
    )


def main():
    print("\n=== FULL PIPELINE TEST (with logging) ===\n")

    orch = build_orchestrator()

    # 1. Drafting
    print("\n--- TEST 1: Drafting short text ---")
    response1 = orch.drafting_short_text(
        "Rewrite this into a polite email: I can’t attend the meeting tomorrow."
    )
    print("\nFINAL OUTPUT:\n")
    print(response1)

    # 2. Research
    print("\n--- TEST 2: Quick research ---")
    response2 = orch.quick_research(
        "What is the difference between machine learning and deep learning?"
    )
    print("\nFINAL OUTPUT:\n")
    print(response2)

    # 3. Planning
    print("\n--- TEST 3: Daily planning ---")
    response3 = orch.daily_planning(
        "Help me plan my workday tomorrow."
    )
    print("\nFINAL OUTPUT:\n")
    print(response3)

    # 4. Memory Summary
    print("\n--- TEST 4: Summarize memory ---")
    response4 = orch.summarize_user_memory()
    print("\nFINAL OUTPUT:\n")
    print(response4)

    print("\n=== END OF FULL PIPELINE TEST ===\n")


if __name__ == "__main__":
    main()