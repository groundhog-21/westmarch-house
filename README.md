# 🏰 **The House of Westmarch**
*A Multi-Agent Concierge Estate of Dubious Decorum*

🧾 Current Version: **v1.0.3 – Domain-Aware Memory Tagging**

[![Kaggle Submission](https://img.shields.io/badge/Kaggle-Submitted-20beff?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/agents-intensive-capstone-project)
[![YouTube Video](https://img.shields.io/badge/YouTube-Video-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=3nJ5RnmqvMk)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/groundhog-21/westmarch-house)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17768826.svg)](https://doi.org/10.5281/zenodo.17768826)

---

Prepared by:

🎩 **Jeeves** — Butler & Orchestrator  
📚 **Perkins** — Valet of Scholarly Inquiry  
✒️ **Miss Pennington** — Secretary & Correspondent  
🕯️ **Lady Hawthorne** — Critic-in-Residence  
👤 **The Master of the Estate** — *you, dear user*

Created by Andrew Gordon Browne
for the Kaggle · Community Hackathon · Agents Intensive - Capstone Project

---

# 🎬 **Project Overview Video**

**📺 YouTube (2 minutes):**  
https://youtu.be/3nJ5RnmqvMk

*A short guided tour of the Estate, its capabilities, and its household staff.*

---

# 👋 **Welcome to the Estate**

Pray, step inside.

**The House of Westmarch** is a fully-fledged multi-agent system disguised as an Edwardian household.  
Instead of issuing commands to CLI scripts, you simply address your staff:

- 🎩 **Jeeves** — planning, orchestration, etiquette, memory, model selection  
- 📚 **Perkins** — research, investigation, tool use  
- ✒️ **Miss Pennington** — drafting, polishing, refinement, transformation  
- 🕯️ **Lady Hawthorne** — critique and rhetorical severity  

Beneath the wallpaper lies an orchestrated, tool-using, stateful, hybrid **Gemini + OpenAI** system  
—with persona logic, memory, and structured workflows.  
On the surface, it is simply a well-run Estate.

---

# 🖥️ **The Estate’s Available Services (Streamlit UI)**

Upon launching the Estate, you will be greeted by the sidebar selector:

### **Choose Mode**
- Parlour Discussions (General Conversation)  
- Arrangements for the Day  
- Matters Requiring Investigation  
- Correspondence & Drafting  
- Records & Summaries from the Archive  
- Her Ladyship’s Critique (Proceed with Caution)  
- Matters Requiring the Whole Household  
- Jeeves Remembers  

Each mode corresponds to a structured orchestrated workflow in  
`westmarch/orchestrator/`.

---

# 🧭 **Architecture Overview**

The Estate is organised into several halls and chambers:

## 🏛️ Orchestration Hall — `westmarch/orchestrator/`
- `router.py` — dispatches requests  
- `workflows.py` — defines multi-agent sequences  
- Shared agentical utilities

## 📚 Core Services — `westmarch/core/`
- `models.py` — Gemini + OpenAI model clients  
- `memory.py` — session + long-term memory  
- `messages.py` — structured schema for internal exchange  
- `tagging.py` — keyword-based domain inference & tag extraction
- Logging, memory tagging, configuration, infrastructure

## 🧑‍🤝‍🧑 Household Staff — `westmarch/agents/`
- `jeeves.py`  
- `perkins.py`  
- `miss_pennington.py`  
- `lady_hawthorne.py`  
- `base_agent.py`

## 🎞️ Demonstrations
- `westmarch/demos/` — technical demonstrations  
- `westmarch/demos_in_universe/` — narrative theatrical demos (1–9)

For detailed diagrams and notes, see:  
`docs/architecture.md`  
`docs/memory.md`  
`docs/personas.md`

---

# 🎭 **In-Universe Demonstrations (1–9)**

Each demonstration is a self-contained narrative illustrating specific agentic features.

Located in `westmarch/demos_in_universe/`:

1. Parlour Discussions — introduction to the staff  
2. Arrangements for the Day — daily planning  
3. Matters Requiring Investigation — teacup psychology  
4. Correspondence & Drafting — chaotic notes rescued by Pennington  
5. Archive Summaries — Jeeves summarises a disastrous project  
6. Her Ladyship’s Critique — “O Languid Moon of Yesteryear”  
7. The Case of the Misbehaving Garden Gnome — multi-agent orchestration  
8. Memory Demonstration — “What Did I Tell You Yesterday?”  
9. **A Mystery in the Archives** — fully automated Streamlit demonstration  

### Demo 9 specifically showcases:
- multi-agent orchestration  
- looped reasoning cycles  
- tool invocation  
- critique escalation  
- long-term memory usage  
- sequential and parallel reasoning  
- pause/resume operations  
- stable theatrical character voices  

---

# 🧪 **Running the Estate**

## **Prerequisites**
- Python **3.11+**  
- API keys for **Gemini** and **OpenAI** stored in `.env`  
- A virtual environment is recommended  

## **Install dependencies**
```bash
pip install -r requirements.txt
```

## **Launch the Household**
```bash
streamlit run app.py
```

Navigate to the URL printed in your terminal (usually:  
`http://localhost:8501`).

You will be welcomed by the assembled staff.

---

# 🗂️ **Repository Layout**

```
westmarch-house/
│
├── app.py                     # Streamlit UI entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This document
├── LICENSE                    # MIT License
├── DISCLAIMER                 # Fictional content disclaimer
├── .gitignore
│
├── docs/                      # Writeups & architecture notes
│   ├── architecture.md
│   ├── architecture_diagram.md
│   ├── demo_9_agentic_features_map.md
│   ├── kaggle_writeup.md
│   ├── memory.md
│   ├── memory_diagram.md
│   ├── personas.md
│   ├── personas_diagram.md
│   └── user_guide.md
│
├── media/                     # Static PNG documentation assets
│   └── images/
│
├── tests/                     # Automated tests
│   ├── test_critique.py
│   ├── test_daily_planning.py
│   ├── test_draft.py
│   ├── test_env.py
│   ├── test_full_pipeline.py
│   ├── test_memory.py
│   ├── test_memory_logging.py
│   ├── test_models.py
│   ├── test_summary.py
│   └── clean_memory.py
│
└── westmarch/                 # Core application
    ├── agents/
    ├── core/
    ├── data/
    ├── demos/
    ├── demos_in_universe/
    ├── orchestrator/
    └── __init__.py
```

All video production materials (Clipchamp project, raw exports, etc.)  
are intentionally excluded and remain local.

---

# 📝 **Technical Write-Up (Required for Review)**

The full competition narrative is located in:

```
docs/kaggle_writeup.md
```

It covers:

- System design  
- Orchestration architecture  
- Agent interactions  
- Memory system  
- Tool invocation and search  
- Demonstration breakdowns  
- Limitations & future directions  

---

# ⚖️ **Licensing & Disclaimer**

- **License:** MIT  
- **Disclaimer:** All characters and behaviours are fictional.  
  No warranty is provided. Exercise reason and decorum.

---

# 🎩 **A Final Note from the Staff**

🎩 **Jeeves:**  
“At any hour, sir, I remain at your disposal.”

📚 **Perkins:**  
“Investigations await! Simply give the word.”

✒️ **Miss Pennington:**  
“I stand ready with paper, ink, and refinement.”

🕯️ **Lady Hawthorne:**  
“Do behave yourself—and write cleanly.”

We remain, as ever,  
**At your service.**