# 🏰 The House of Westmarch
### *A Fully Staffed, Mildly Unhinged Multi-Agent Concierge*
**Track:** Concierge Agents

🎩 Jeeves · 📚 Perkins · ✒️ Miss Pennington · 🕯️ Lady Hawthorne · 👤 The Master

---

## Project Description

**The House of Westmarch** is a gamified, narrative-driven multi-agent concierge system disguised as an Edwardian household. Beneath the humor and theatrics lies a fully-engineered agentic platform that provides daily assistance. Users delegate tasks to “household staff,” creating an immersive experience that is both technically robust and unexpectedly entertaining.

---

## 1. Problem Statement

Modern users constantly manage small but cognitively taxing tasks: planning, researching, drafting, critiquing, and remembering previous conversations. These responsibilities accumulate until the user effectively becomes their own secretary, researcher, editor, and archivist.

Westmarch reframes these burdens through narrative delegation:

- 🎩 **Jeeves** handles orchestration, planning, etiquette, and memory  
- 📚 **Perkins** conducts structured research and fact-based analysis  
- ✒️ **Miss Pennington** transforms rough notes into polished writing  
- 🕯️ **Lady Hawthorne** provides incisive literary critique  

The result is a system that lightens cognitive load while engaging the user through a theatrical, humorous metaphor.

---

## 2. Solution Overview

Westmarch blends narrative charm with serious engineering. The system includes:

- Multi-agent coordination via a central orchestrator  
- Hybrid Gemini + OpenAI model selection  
- Long-term memory with domain-aware filtering  
- Tool-assisted research (Perkins)  
- Polished drafting (Miss Pennington)  
- Critique loops (Hawthorne)  
- Workflow-based reasoning patterns  
- A polished, intuitive Streamlit front-end  

The UI offers eight selectable modes, each mapping to an orchestrated workflow—making the system approachable for non-technical users while maintaining technical depth for judges and reviewers.

---

## 3. Architecture Overview  
Westmarch’s architecture consists of five major layers, each corresponding directly to the repository structure.

---

### 3.1 Orchestration — `westmarch/orchestrator/`

**Files:**
- `router.py` — selects the correct workflow based on UI mode  
- `workflows.py` — defines sequential, parallel, and looped agent interactions   

**Role:**  
Jeeves routes every request through these orchestrated flows, including Demo 9’s multi-stage automation.

---

### 3.2 Core Services — `westmarch/core/`

**Files:**
- `models.py` — configures Gemini & OpenAI model clients  
- `memory.py` — long-term + session memory engine  
- `messages.py` — structured message schemas  
- `logging.py` — detailed workflow logs  
- `tagging.py` — domain inference + auto-tagging  

**Role:**  
Implements the foundational machinery for agent behavior, context handling, memory, and observability.

---

### 3.3 Agents — `westmarch/agents/`

**Files:**
- `base_agent.py` — shared parent class for all agents  
- `jeeves.py` — orchestrator persona  
- `perkins.py` — research agent  
- `miss_pennington.py` — drafting & archiving agent  
- `lady_hawthorne.py` — critique agent  
- `prompts_jeeves.py` — persona prompt templates  

**Role:**  
Defines the four household staff personas with consistent stylistic voices and workflow responsibilities.

---

### 3.4 Memory Layer — `westmarch/data/memory.json`

**File:**
- `memory.json` — persistent long-term memory store  

**Features:**
- keyword scoring  
- semantic tag inference  
- domain filtering  
- continuity recall  
- persona-aware retrieval  

**Role:**  
Allows Jeeves to retrieve previous discussions, track topics over time, and answer questions such as:  
*“What did I tell you yesterday about my poem?”*

---

### 3.5 Front-End — `app.py`

**File:**
- `app.py` — Streamlit UI  

**Features:**
- eight selectable interaction modes  
- full single-click automation for Demo 9  
- integrated “How to Run the Demos” page  
- agent avatars and chat transcript display  
- footer links to documentation  

---

## 4. Key Agentic Features

Westmarch implements more than the required agentic elements:

- **Multi-agent system** (Jeeves, Perkins, Miss Pennington, Hawthorne)  
- **Sequential + parallel workflows** (notably Demo 9)  
- **Tool usage** (Perkins + memory engine)  
- **Long-term memory** with tagging and domain inference  
- **Context engineering** (mode routing, persona prompts)  
- **Observability** (logging hooks)  

---

## 5. Demonstrations (1–9)

### Demo 1 — Parlour Discussions  
Introductory conversation and persona grounding.

### Demo 2 — Arrangements for the Day  
Planning workflow run by Jeeves.

### Demo 3 — Matters Requiring Investigation  
Structured analysis via Perkins.

### Demo 4 — Correspondence & Drafting  
Miss Pennington rewrites rough notes.

### Demo 5 — Records & Summaries
Jeeves retrieves archival summaries.

### Demo 6 — Her Ladyship’s Critique  
Elegant critique of user text.

### Demo 7 — Misbehaving Garden Gnome  
A complex multi-agent escalation.

### Demo 8 — Memory Continuity  
Long-term memory in action.

### Demo 9 — A Mystery in the Archives  
Fully automated narrative featuring:

- looping research  
- critique cycles  
- metadata scrutiny  
- hybrid model usage  
- dramatic reveal  

---

## 6. Value & Impact

### Practical Value
- Structured planning  
- Improved writing  
- High-quality research  
- Long-term conversational memory  

### Experiential Value
Narrative framing enhances adoption and delight.

As the staff put it:
- “Clarity is but a request away.” — Perkins  
- “No more wrestling with blank pages.” — Miss Pennington  
- “The prose improves.” — Lady Hawthorne  
- “The Estate restores dignity to everyday tasks.” — Jeeves  

---

## 7. Quick Start

To run the demonstrations locally:

1\. Clone the repository  
2\. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3\. Launch the Streamlit interface:  
   ```
   streamlit run app.py
   ```
4\. Navigate to the URL printed in your terminal (usually:  
`http://localhost:8501`).

(You will be welcomed by the assembled staff.)


5\. For manual demos (1–8):  
   Select the correct sidebar mode and follow the scripted prompts found in  
   `westmarch/demos_in_universe/`

6\. For the fully automated flagship demo (Demo 9):  
   Select **“Matters Requiring the Whole Household”** from the sidebar  
   and press the button **“▶ Run Demo 9 – A Mystery in the Archives”** near the top of the screen.

➡️ Full instructions:  
[How to Run Demos (1–9)](https://github.com/groundhog-21/westmarch-house/blob/main/docs/how_to_run_demos.md)

---

## 8. Conclusion

**The House of Westmarch** blends theatrical charm with serious agentic workflows.  
Its multi-agent orchestration, memory system, tool use, critique loops, and narrative demonstrations offer a complete, intuitive, and judge-friendly exploration of modern agent design.

🕯️ *Lady Hawthorne:*  
“If this does not satisfy the judges, nothing will.”