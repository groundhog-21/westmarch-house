# westmarch/demos/demo_research.py

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

    question = "What is the difference between ETFs and mutual funds?"

    print("\n=== DEMO: Quick Research ===\n")
    print("USER QUESTION:\n")
    print(question)

    result = orch.quick_research(question)

    print("\nASSISTANT OUTPUT:\n")
    print(result)
    print("\n=== END DEMO ===\n")


if __name__ == "__main__":
    main()