# westmarch/demos/test_critique.py

from westmarch.core.models import ModelClient
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.orchestrator.workflows import WestmarchOrchestrator


def build_orchestrator():
    jeeves = JeevesAgent(ModelClient("Jeeves"))
    perkins = PerkinsAgent(ModelClient("Perkins"))
    pennington = MissPenningtonAgent(ModelClient("Miss Pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient("Lady_Hawthorne"))

    return WestmarchOrchestrator(
        jeeves=jeeves,
        perkins=perkins,
        pennington=pennington,
        hawthorne=hawthorne,
    )


def main():
    print("=== CRITIQUE WORKFLOW TEST ===\n")

    test_text = """
    The quarterly report is fine. We met most goals,
    though a few deliverables were delayed. Overall, it is acceptable.
    """

    orchestrator = build_orchestrator()

    result = orchestrator.critique_text(test_text)

    print("\nFINAL CRITIQUE OUTPUT:\n")
    print(result)
    print("\n=== END TEST ===")


if __name__ == "__main__":
    main()