# westmarch/demos/demo_multi_agent_chain.py

"""
Demo: Grand Household Conference — Full Multi-Agent Orchestration

Scenario:
The Patron asks for a refined overview of recent developments in agentic AI.
The full Westmarch Household collaborates:

1. Patron → Jeeves: request
2. Jeeves → Perkins: research delegation
3. Perkins → Jeeves: research findings
4. Jeeves → Miss Pennington: drafting request
5. Miss Pennington → Jeeves: polished draft
6. Jeeves → Lady Hawthorne: request for critique
7. Lady Hawthorne → Jeeves: critique
8. Jeeves → Patron: final synthesized answer

Run with:
    python -m westmarch.demos.demo_multi_agent_chain
"""

from westmarch.orchestrator.workflows import WestmarchOrchestrator
from westmarch.agents.jeeves import JeevesAgent
from westmarch.agents.perkins import PerkinsAgent
from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.agents.lady_hawthorne import LadyHawthorneAgent
from westmarch.core.models import ModelClient
from westmarch.core.messages import AgentMessage, Context, TaskType


# -------------------------
# Helper functions
# -------------------------

def banner(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70 + "\n")


def section(title: str):
    print("\n" + "━" * 70)
    print(title)
    print("━" * 70 + "\n")


def build_orchestrator() -> WestmarchOrchestrator:
    """Constructs all agents and the orchestrator, as in the main app."""
    jeeves = JeevesAgent(ModelClient("jeeves"))
    perkins = PerkinsAgent(ModelClient("perkins"))
    pennington = MissPenningtonAgent(ModelClient("miss_pennington"))
    hawthorne = LadyHawthorneAgent(ModelClient("lady_hawthorne"))

    return WestmarchOrchestrator(
        jeeves=jeeves,
        perkins=perkins,
        pennington=pennington,
        hawthorne=hawthorne,
    )


# -------------------------
# Main demo logic
# -------------------------

def run_demo():
    banner("🏰 Grand Household Conference — Multi-Agent Orchestration Demo")

    orchestrator = build_orchestrator()
    jeeves = orchestrator.jeeves
    perkins = orchestrator.perkins
    pennington = orchestrator.pennington
    hawthorne = orchestrator.hawthorne

    # 0) Patron's request
    section("👤 Patron → Jeeves: Initial Request")

    patron_request = (
        "Jeeves, my good fellow, I require a clear and well-structured overview of "
        "recent developments in so-called 'agentic AI' over roughly the last year. "
        "Please consult the household staff as needed — Perkins for investigation, "
        "Miss Pennington for drafting, and if appropriate, invite Lady Hawthorne to "
        "offer her perspective. I should like something both informative and "
        "pleasant to read."
    )
    print(patron_request)

    # 1) Jeeves acknowledges & outlines the plan
    section("Jeeves: Acknowledgement & Plan of Action")

    jeeves_msg = AgentMessage(
        sender="User",
        recipient="Jeeves",
        task_type=TaskType.MIXED,
        content=(
            "Please briefly acknowledge the patron's request and outline, in "
            "3–5 sentences, how you intend to involve the household staff to "
            "fulfil it."
        ),
        context=Context(original_user_request=patron_request, previous_outputs=[]),
    )
    jeeves_plan = jeeves.run(jeeves_msg)
    print(jeeves_plan)

    # 2) Jeeves → Perkins: research delegation
    section("Jeeves → Perkins: Research Delegation")

    to_perkins = AgentMessage(
        sender="Jeeves",
        recipient="Perkins",
        task_type=TaskType.RESEARCH,
        content=(
            "The patron requests an overview of recent developments in 'agentic AI' "
            "over roughly the last year. Please investigate key themes, notable "
            "advances, example applications, and any emerging challenges or open "
            "questions. Summarize your findings clearly in bullet points or short "
            "sections suitable for later drafting."
        ),
        context=Context(original_user_request=patron_request, previous_outputs=[]),
    )
    perkins_research = perkins.run(to_perkins)
    print(perkins_research)

    # 3) Perkins → Jeeves: research summary (already printed)
    #    Now Jeeves forwards this to Miss Pennington for drafting.
    section("Jeeves → Miss Pennington: Drafting Request")

    to_pennington = AgentMessage(
        sender="Jeeves",
        recipient="Miss Pennington",
        task_type=TaskType.DRAFTING,
        content=(
            "Using the research summary provided below, please draft a polished, "
            "patron-ready overview of recent developments in agentic AI. "
            "Aim for a tone that is clear, informative, and gently formal, "
            "as if preparing a briefing for an educated layperson.\n\n"
            "RESEARCH SUMMARY FROM PERKINS:\n"
            f"{perkins_research}"
        ),
        context=Context(
            original_user_request=patron_request,
            previous_outputs=[{"research_summary": perkins_research}],
        ),
    )
    pennington_draft = pennington.run(to_pennington)

    print(pennington_draft)

    # 4) Jeeves → Lady Hawthorne: critique of the draft
    section("Jeeves → Lady Hawthorne: Request for Critique")

    # We reuse the orchestrator's refined critique workflow so that
    # Lady Hawthorne critiques the draft, and Jeeves presents her verdict.
    critique_input = (
        "This is Miss Pennington's draft report on recent developments in agentic AI. "
        "Please critique its clarity, structure, and tone:\n\n"
        f"{pennington_draft}"
    )
    hawthorne_critique = orchestrator.critique_text(critique_input)

    print(hawthorne_critique)

    # 5) Jeeves synthesizes everything into a final answer for the Patron
    section("Jeeves → Patron: Final Synthesized Answer")

    final_msg = AgentMessage(
        sender="System",
        recipient="Jeeves",
        task_type=TaskType.MIXED,
        content=(
            "Using the original patron request, Perkins' research summary, "
            "Miss Pennington's draft, and Lady Hawthorne's critique, please "
            "compose a final, coherent response for the patron. "
            "The response should:\n"
            "- Briefly reassure the patron that the household has collaborated.\n"
            "- Provide a clear overview of developments in agentic AI.\n"
            "- Integrate improvements suggested implicitly by Lady Hawthorne.\n"
            "- Be structured with short sections or headings.\n\n"
            f"ORIGINAL REQUEST:\n{patron_request}\n\n"
            f"RESEARCH SUMMARY (PERKINS):\n{perkins_research}\n\n"
            f"DRAFT (MISS PENNINGTON):\n{pennington_draft}\n\n"
            f"CRITIQUE (LADY HAWTHORNE VIA JEEVES):\n{hawthorne_critique}\n"
        ),
        context=Context(
            original_user_request=patron_request,
            previous_outputs=[
                {"research": perkins_research},
                {"draft": pennington_draft},
                {"critique": hawthorne_critique},
            ],
        ),
    )

    final_answer = jeeves.run(final_msg)
    print(final_answer)

    banner("🏁 End of Grand Household Conference Demo")


if __name__ == "__main__":
    run_demo()