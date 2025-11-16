# westmarch/demos/cli_demo.py
from __future__ import annotations

from westmarch.core.models import ModelClient
from westmarch.core.messages import TaskType
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.orchestrator.router import classify_task
from westmarch.orchestrator.workflows import WestmarchOrchestrator


def build_orchestrator():
    jeeves_client = ModelClient("Jeeves")
    perkins_client = ModelClient("Perkins")
    pennington_client = ModelClient("Miss Pennington")
    hawthorne_client = ModelClient("Lady_Hawthorne")

    jeeves = JeevesAgent(jeeves_client)
    perkins = PerkinsAgent(perkins_client)
    pennington = MissPenningtonAgent(pennington_client)
    hawthorne = LadyHawthorneAgent(hawthorne_client)

    return WestmarchOrchestrator(jeeves, perkins, pennington, hawthorne)


def main():
    orch = build_orchestrator()
    print("Welcome to Westmarch House. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in {"quit", "exit"}:
            print("Jeeves: Very good, sir/madam. Until next time.")
            break

        task = classify_task(user_input)

        if task == TaskType.PLANNING:
            response = orch.daily_planning(user_input)
        elif task == TaskType.RESEARCH:
            response = orch.quick_research(user_input)
        elif task == TaskType.DRAFTING:
            response = orch.drafting_short_text(user_input)
        else:
            response = orch.daily_planning(user_input)

        print(f"\nWestmarch:\n{response}\n")


if __name__ == "__main__":
    main()