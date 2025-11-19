# 🏰 The House of Westmarch  
*A Multi-Agent Estate for the Conduct of Daily Affairs*  

Prepared by:  
- 🎩 Jeeves — Butler & Orchestrator  
- 📚 Perkins — Valet of Scholarly Inquiry  
- ✒️ Miss Pennington — Secretary & Correspondent  
- 🕯️ Lady Hawthorne — Critic-in-Residence  
- 👤 The Master of the Estate (you, dear user)  

---

## Welcome to the Estate

Pray, step inside.

**The House of Westmarch** is a multi-agent system disguised as a well-run Edwardian household.  
Instead of tabs and command-line flags, you have **staff**:

- 🎩 *Jeeves* handles planning, orchestration, and memory.  
- 📚 *Perkins* conducts research with an alarming zeal.  
- ✒️ *Miss Pennington* turns your chaotic notes into polished prose.  
- 🕯️ *Lady Hawthorne* critiques anything you dare to show her.

Behind the wallpaper, this is a Gemini-powered, orchestrated, tool-using, stateful agent system.  
On the surface, it is an Estate where you ring for the butler.

---

## The Estate’s Available Services (Streamlit UI)

Running the application presents a sidebar titled **“The House of Westmarch”** with:

- 🎩 **Parlour Discussions** – General conversation with Jeeves.  
- 🎩 **Arrangements for the Day** – Daily planning and prioritisation.  
- 📚 **Matters Requiring Investigation** – Research and analysis by Perkins.  
- ✒️ **Correspondence & Drafting** – Polished emails, letters, and notes by Miss Pennington.  
- 🎩 **Records & Summaries from the Archive** – Summaries and digests prepared by Jeeves.  
- 🕯️ **Her Ladyship’s Critique** – Literary critique and evaluation from Lady Hawthorne.

Each selection routes your request through the appropriate **agent workflow**.

---

## Architecture (At a Glance)

The Estate is arranged as follows:

- **Orchestration Hall** — `westmarch/orchestrator/`  
  - `router.py` decides which staff member should respond.  
  - `workflows.py` runs multi-agent chains (e.g., research → drafting → critique).

- **Core Services** — `westmarch/core/`  
  - `models.py` selects and configures Gemini models.  
  - `memory.py` maintains session and long-term memory (see `westmarch/data/memory.json`).  
  - `messages.py` defines internal message formats.  
  - `logging.py` supports observability and debugging.

- **Household Staff** — `westmarch/agents/`  
  - `jeeves.py` — planner and orchestrator, also your primary conversational partner.  
  - `perkins.py` — research valet; structured investigations with tools.  
  - `miss_pennington.py` — drafting and summarisation.  
  - `lady_hawthorne.py` — critique and evaluation.  
  - `base_agent.py` — common behaviour for all staff.

- **Demonstrations**  
  - Technical demos: `westmarch/demos/`  
  - In-universe scripts: `westmarch/demos_in_universe/` (see below).

---

## In-Universe Demonstrations

For the benefit of the Guild of Kaggle (and any visiting dignitaries), the Estate includes eight theatrical demonstration scripts in:

`westmarch/demos_in_universe/`

1. **Parlour Discussions** — Introduction to the staff.  
2. **Arrangements for the Day** — Daily planning with Jeeves.  
3. **Matters Requiring Investigation** — Teacup psychology with Perkins.  
4. **Correspondence & Drafting** — Miss Pennington rescues a shambles of notes.  
5. **Records & Summaries from the Archive** — Jeeves summarises a disastrous household project.  
6. **Her Ladyship’s Critique** — Lady Hawthorne reviews “O Languid Moon of Yesteryear.”  
7. **The Case of the Misbehaving Garden Gnome** — Grand multi-agent orchestration.  
8. **Memory Demonstration** — “What Did I Tell You Yesterday?”, showcasing state and recall.

Each script is a standalone narrative, designed to be read alongside the UI and source code to understand how the system behaves.

---

## Running the Estate

### Prerequisites

- Python 3.11+  
- A valid OpenAI / Gemini API key configured in `.env` (not committed)  
- Recommended: a virtual environment

### Installation

```bash
pip install -r requirements.txt
```

### Launching the House of Westmarch

```bash
streamlit run app.py
```
Then visit the URL printed in your terminal (typically http://localhost:8501) and step into the Estate.

### Repository Layout

WESTMARCH-HOUSE/
├── app.py                # Streamlit UI entry point
├── requirements.txt      # Python dependencies
├── README.md             # This very document
├── LICENSE               # MIT License
├── DISCLAIMER            # In-universe content & usage disclaimer
├── assets/               # Images (thumbnail, diagrams, screenshots)
├── docs/                 # Kaggle writeup, architecture notes, video script, etc.
└── westmarch/            # Core application package
    ├── agents/           # Jeeves, Perkins, Miss Pennington, Lady Hawthorne
    ├── core/             # Models, memory, logging, messages
    ├── data/             # memory.json
    ├── demos/            # Technical demos and tests
    ├── demos_in_universe/ # Narrative demonstration scripts
    ├── orchestrator/     # Router and workflows
    └── tests/            # Automated tests for key behaviour

---

## Licensing & Disclaimer

- License: MIT (see LICENSE).
- Disclaimer: see DISCLAIMER for important notes about fictionality and warranty

In brief:
This is a fictional, gamified multi-agent demonstration.
All characters are fictional. Any resemblance to real persons is unintended.
No warranty is provided; use is at your own discretion and peril.

---

## A Note from the Staff

🎩 Jeeves:
“Should you wish to extend the Estate — add new staff, tools, or rooms — you are most welcome. I shall be delighted to co-ordinate them.”

📚 Perkins:
“I would be honoured to assist with further research agents, sir.”

✒️ Miss Pennington:
“I stand ready to polish any additional documentation you devise.”

🕯️ Lady Hawthorne:
“If you insist on adding more code, do endeavour to make it readable.”

We remain, as ever,
At your service.

---





