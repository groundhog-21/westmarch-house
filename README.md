🏰 **The House of Westmarch**  
*A Multi-Agent Estate for the Conduct of Daily Affairs*

Prepared by:

🎩 **Jeeves** — Butler & Orchestrator  
📚 **Perkins** — Valet of Scholarly Inquiry  
✒️ **Miss Pennington** — Secretary & Correspondent  
🕯️ **Lady Hawthorne** — Critic-in-Residence  
👤 **The Master of the Estate** — *you, dear user*

---

# **Welcome to the Estate**

Pray, step inside.

**The House of Westmarch** is a fully-fledged, multi-agent system disguised as an Edwardian household.  
Instead of command-line flags and API chains, you issue direction to your staff:

- 🎩 **Jeeves** handles planning, orchestration, memory, and etiquette.  
- 📚 **Perkins** conducts research with great zeal (and occasionally alarm).  
- ✒️ **Miss Pennington** transforms chaos into polished prose.  
- 🕯️ **Lady Hawthorne** critiques with immaculate severity.  

Behind the wallpaper lies a **Gemini-powered + OpenAI-powered**, orchestrated, tool-using, stateful multi-agent system.  
On the surface, however, it is an Estate where one simply rings for the butler.

---

# 🖥️ **The Estate’s Available Services (Streamlit UI)**

Upon launching the Estate, you will be greeted by the sidebar selector:

### **Choose Mode**
- **Parlour Discussions (General Conversation)**  
- **Arrangements for the Day**  
- **Matters Requiring Investigation**  
- **Correspondence & Drafting**  
- **Records & Summaries from the Archive**  
- **Her Ladyship's Critique (Proceed with Caution)**  
- **Matters Requiring the Whole Household**  
- **Jeeves Remembers**

These correspond precisely to the agent workflows defined in `westmarch/orchestrator/`.  
Selecting a mode routes your input through the correct chain of agents and tools.

---

# 🧭 **Architecture Overview**

The Estate is arranged as follows:

## 🏛️ **Orchestration Hall — `westmarch/orchestrator/`**
- **router.py** — dispatches requests to the appropriate staff  
- **workflows.py** — defines structured multi-agent sequences  
  (e.g., *research → drafting → critique → summarisation*)

## 📚 **Core Services — `westmarch/core/`**
- **models.py** — configures **Gemini 1.5** and **OpenAI** model clients  
- **memory.py** — session & long-term memory (stored in `westmarch/data/`)  
- **messages.py** — structured internal message schema  
- **logging.py** — observability & debug utilities  

## 🧑‍🤝‍🧑 **Household Staff — `westmarch/agents/`**
- 🎩 **jeeves.py** — planner, orchestrator, etiquette engine  
- 📚 **perkins.py** — research valet; investigative reasoning & tool use  
- ✒️ **miss_pennington.py** — drafting, refinement, rewriting, summarisation  
- 🕯️ **lady_hawthorne.py** — critique, rhetorical evaluation, literary inspection  
- **base_agent.py** — shared behaviours, message formats, tool invocation  

## 🎞️ **Demonstrations**
- **Technical demos:** `westmarch/demos/`  
- **In-universe theatrical demos:** `westmarch/demos_in_universe/`  

---

# 🎭 **In-Universe Demonstrations (Demos 1–9)**

Each demonstration is a standalone narrative designed to illustrate particular agent capabilities, including memory, multi-agent routing, critique, and structured investigation.

Located in `westmarch/demos_in_universe/`:

1. **Parlour Discussions** — Introduction to the staff  
2. **Arrangements for the Day** — Daily planning  
3. **Matters Requiring Investigation** — Teacup psychology  
4. **Correspondence & Drafting** — Chaotic notes rescued by Miss Pennington  
5. **Archive Summaries** — Jeeves summarises a disastrous household project  
6. **Her Ladyship’s Critique** — “O Languid Moon of Yesteryear”  
7. **The Case of the Misbehaving Garden Gnome** — Multi-agent orchestration  
8. **Memory Demonstration** — “What Did I Tell You Yesterday?”  
9. **A Mystery in the Archives** — *fully automated demo run through Streamlit*  

Demo 9 showcases:

- multi-agent orchestration  
- looped reasoning  
- state transitions  
- critique escalation  
- tool use  
- archival metadata analysis  
- pause/resume logic  
- theatrical voice consistency  

---

# 🧪 **Running the Estate**

## **Prerequisites**
- Python **3.11+**  
- API keys for **Gemini** *and* **OpenAI**, stored in `.env`  
- A virtual environment is recommended  

## **Install dependencies**
```bash
pip install -r requirements.txt
```

## **Launch the Household**
```bash
streamlit run app.py
```

Navigate to the terminal’s printed URL (usually `http://localhost:8501`).  
You will be welcomed by the assembled staff.

---

# 🏛️ **Repository Layout**

```
westmarch-house/
│
├── app.py                     # Streamlit UI entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This document
├── LICENSE                    # MIT License
├── DISCLAIMER                 # Fictional content disclaimer
│
├── assets/                    # UI assets, diagrams, thumbnails
├── docs/                      # Kaggle writeup, architecture notes, video script
│
└── westmarch/                 # Core application package
    ├── agents/                # Jeeves, Perkins, Miss Pennington, Lady Hawthorne
    ├── core/                  # Models, memory system, message formatting
    ├── data/                  # memory.json & related state
    ├── demos/                 # Technical demonstrations
    ├── demos_in_universe/     # Narrative theatrical scripts (1–9)
    ├── orchestrator/          # Routing and multi-agent workflows
    └── tests/                 # Automated behavioural tests
```

---

# 🎬 **Video Demonstration**

*(Link to be added upon upload — required for Kaggle submission.)*  
Runtime target: **2–3 minutes**, with **Jeeves narration**.

---

# 📄 **Write-Up Summary (Required for Review)**

A comprehensive technical writeup is included in:

```
docs/kaggle_writeup.md
```

It covers:

- System design  
- Multi-agent reasoning  
- Memory & state  
- Tool invocation  
- Orchestration patterns  
- Demo breakdowns  
- Challenges & limitations  

---

# ⚖️ **Licensing & Disclaimer**

- **License:** MIT  
- **Disclaimer:** All characters, voices, and behaviours are fictional.  
  No warranty is provided. Use at your own discretion.

---

# 🎩 **A Final Note from the Staff**

🎩 **Jeeves:**  
“Should you wish to expand the Estate — perhaps a librarian, a gardener, or a historian — I remain at your command.”

📚 **Perkins:**  
“I stand ready for further investigative duties, sir.”

✒️ **Miss Pennington:**  
“Do call upon me for drafts, summaries, or documentation refinements.”

🕯️ **Lady Hawthorne:**  
“If you *must* write more code, at least ensure it is readable.”

We remain, as ever,  
**At your service.**