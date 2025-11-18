# westmarch/demos/demo_memory_summary.py

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

    print("\n=== DEMO: Memory Summary ===\n")
    print("This demo summarizes what the household currently remembers about you.\n")

    result = orch.summarize_user_memory()

    print("ASSISTANT OUTPUT:\n")
    print(result)
    print("\n=== END DEMO ===\n")


if __name__ == "__main__":
    main()