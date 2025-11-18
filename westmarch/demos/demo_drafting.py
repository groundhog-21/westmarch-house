# westmarch/demos/demo_drafting.py

from westmarch.core.models import ModelClient
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.orchestrator.workflows import WestmarchOrchestrator


def build_orchestrator() -> WestmarchOrchestrator:
    jeeves = JeevesAgent(ModelClient("Jeeves"))
    perkins = PerkinsAgent(ModelClient("Perkins"))
    pennington = MissPenningtonAgent(ModelClient("Miss Pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient("Lady_Hawthorne"))
    return WestmarchOrchestrator(jeeves, perkins, pennington, hawthorne)


def main():
    orch = build_orchestrator()

    user_text = (
        "Rewrite this into a polite email: "
        "I need the slides today or we’ll miss the deadline."
    )

    print("\n=== DEMO: Drafting Short Text ===\n")
    print("USER INPUT:\n")
    print(user_text)

    result = orch.drafting_short_text(user_text)

    print("\nASSISTANT OUTPUT:\n")
    print(result)
    print("\n=== END DEMO ===\n")


if __name__ == "__main__":
    main()