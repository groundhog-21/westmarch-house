from westmarch.orchestrator.workflows import WestmarchOrchestrator
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.core.models import ModelClient


def build_orchestrator() -> WestmarchOrchestrator:
    """Mirror the initialization logic from app.py, without Streamlit."""
    jeeves = JeevesAgent(ModelClient(agent_name="Jeeves"))
    perkins = PerkinsAgent(ModelClient(agent_name="Perkins"))
    pennington = MissPenningtonAgent(ModelClient(agent_name="Miss Pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient(agent_name="Lady Hawthorne"))

    return WestmarchOrchestrator(
        jeeves=jeeves,
        perkins=perkins,
        pennington=pennington,
        hawthorne=hawthorne,
    )


if __name__ == "__main__":
    orc = build_orchestrator()

    # TEST A — User provides a structured schedule (Jeeves should *preserve* it)
    print("\n=== TEST A — User Provided Schedule ===")
    result_a = orc.daily_planning(
        "8:00–11:30 Kaggle; 1–2:30 shopping; 3–5 reading; 8–9 Grantchester"
    )
    print(result_a)

    # TEST B — User gives no times (Jeeves should *propose* a schedule)
    print("\n=== TEST B — Jeeves Proposes Schedule ===")
    result_b = orc.daily_planning("Jeeves, help me plan my day.")
    print(result_b)