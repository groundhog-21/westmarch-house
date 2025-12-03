# 🏰 The House of Westmarch — Architectural Overview
*A Multi‑Agent Concierge Estate of Dubious Decorum*

This document describes how the Estate is constructed behind the scenes — with a focus on **orchestration, agents, and the updated domain‑aware memory system**.

---

## 1. High‑Level System View (Verbal Diagram)

User 👤 interacts via the **Streamlit UI** in `app.py` →  
Request is packaged and sent to the **Westmarch Orchestrator** →  
The orchestrator consults **Jeeves** 🎩, who selects a workflow and delegates to staff →

- Research & analysis → 📚 **Perkins**  
- Drafting, summaries, records → ✒️ **Miss Pennington**  
- Critique & evaluation → 🕯️ **Lady Hawthorne**  
- Planning, routing, memory recall → 🎩 **Jeeves** himself  

Along the way, agents may:

- Call tools (e.g. models, metadata scanners)  
- Read from or write to **persistent memory**  
- Hand work off to other agents in sequential or parallel steps  

Final responses are returned to Jeeves, who frames the reply for the Patron 👤.

Long‑term memory is stored as JSON in:

```text
westmarch/data/memory.json
```

Domain‑aware tagging and recall logic live in:

```text
westmarch/core/memory.py
westmarch/core/tagging.py
```

---

## 2. Package Map

The Estate is divided into several “wings”, each implemented as a Python package.

---

### 2.1 `westmarch/agents/` — Household Staff

Implements the four primary persona agents and shared base logic.

- `base_agent.py`  
  - Shared helpers for all staff (LLM calls, formatting, tool hooks).  

- `jeeves.py` 🎩  
  - Head Butler & Orchestrator interface.  
  - Primary entry point for workflows (“Parlour Discussions”, planning, memory recall).  
  - Coordinates with the other agents and reads from memory.  

- `perkins.py` 📚  
  - Research Footman.  
  - Produces structured, numbered analyses and anomaly reports.  
  - May be invoked standalone (research mode) or as part of household workflows.  

- `miss_pennington.py` ✒️  
  - Scribe & Archivist.  
  - Drafts and refines letters, notes, reports, and summaries.  
  - Acts as **memory writer**: uses `MemoryBank` + tagging utilities to save structured entries.  

- `lady_hawthorne.py` 🕯️  
  - Critic‑in‑Residence (OpenAI‑backed).  
  - Delivers concise, sharp critique used in dedicated critique mode and in multi‑agent demos.  

Personas are described more fully in:

```text
docs/personas.md
docs/personas_diagram.md
```

---

### 2.2 `westmarch/core/` — Core Services & Memory

This package provides shared infrastructure: models, memory, tagging, messaging, and logging.

- `models.py`  
  - Configures **Gemini** and **OpenAI** clients.  
  - Encapsulates model selection per agent (e.g. Hawthorne → OpenAI).  

- `memory.py`  
  - Defines the `MemoryBank` abstraction for JSON‑backed persistence.  
  - Implements:
    - `load_all()` / `save_entry()`  
    - Structured logging of reads/writes  
    - The **Jeeves Remembers** recall pipeline  
    - Scoring and ranking of candidate memories  
    - Integration with the domain‑inference utilities in `tagging.py`  

- `tagging.py`  ✅ *(new in v1.0.3)*  
  - Central home for **keyword‑based domain inference** and **tag extraction**.  
  - Maintains the `DOMAIN_KEYWORDS` mapping (e.g. `poetry`, `finance`, `gnome`, `schedule`).  
  - Provides helper functions used to:
    - Infer domains from user input and memory content  
    - Attach `domain:*` tags when saving new entries  
    - Support domain‑coherent recall in the memory pipeline  

- `messages.py`  
  - Defines internal message formats and helper classes.  
  - Keeps agent↔orchestrator communication structured and explicit.  

- `logging.py`  
  - Sets up logging configuration used throughout the system.  
  - Produces consistent, human‑readable traces such as:
    - `WORKFLOW: …`  
    - `MEMORY: …`  
    - `MEMORY‑RECALL: …`  

Together, `memory.py` and `tagging.py` constitute the **modern memory layer**: a JSON store plus a small but effective semantic “router” for recall.

---

### 2.3 `westmarch/orchestrator/` — Orchestration Hall

This package encodes the high‑level flows that make the Estate feel coherent and theatrical.

- `router.py`  
  - Translates the user’s selected **mode** (e.g. “Her Ladyship’s Critique”) into an internal workflow name.  
  - Provides a single `run(...)` entry point used by `app.py`.  

- `workflows.py`  
  - Defines concrete multi‑step workflows for each mode:  
    - Parlour discussions  
    - Daily planning  
    - Research investigations  
    - Drafting and correspondence  
    - Archive summaries  
    - Critique sessions  
    - Memory recall (`recall_memory`)  
    - Whole‑household demos (including **Demo 9 – A Mystery in the Archives**)  
  - Orchestrates sequences like:
    - *Perkins → Pennington → Hawthorne → Jeeves*  
    - Parallel analysis rounds followed by a summarising council  

The orchestrator is deliberately thin but explicit, so judges and users can see **exactly** how agents are combined.

---

### 2.4 `westmarch/data/` — Persistent State

- `memory.json`  
  - JSON list of entries:
    ```json
    {
      "timestamp": "2025-12-02T05:00:12.899113",
      "content": "Daily plan created based on user request: …",
      "tags": [
        "auto",
        "domain:schedule",
        "type:planning"
      ]
    }
    ```
  - Populated by Miss Pennington via `MemoryBank.save_entry(...)`.  
  - Tags are a combination of:
    - Automatically inferred **domain tags** (e.g. `domain:gnome`, `domain:poetry`)  
    - Workflow‑specific tags (e.g. `type:parlour`, `type:critique`)  
    - A default `"auto"` tag for all auto‑generated entries  

The file is designed to remain human‑readable for inspection and debugging.

---

### 2.5 Front‑End: `app.py` — Streamlit Estate Entrance

The Streamlit application is the public entrance to the Estate.

- Renders the sidebar with **mode selector** and title.  
- Displays the chat transcript with avatars:
  - 👤 user / Patron  
  - 🎩 Jeeves  
  - 📚 Perkins  
  - ✒️ Miss Pennington  
  - 🕯️ Lady Hawthorne  
  - 🏰 Fallback / system  
- Dispatches user input to the orchestrator:
  ```python
  result = orchestrator.run("parlour_discussion", prompt, selected_mode=mode)
  ```
- Hosts the **Demo 9** button when  
  `Matters Requiring the Whole Household` is selected.  

Custom CSS is used to apply the **EB Garamond** typeface and gentle theming, while preserving Streamlit’s core behaviour.

---

### 2.6 Documentation, Tests, and Media

Outside the main application packages:

- `docs/` — architecture, personas, memory, user guide, Kaggle writeup.  
- `tests/` — automated tests for models, memory, logging, and core workflows.  
- `media/images/` — PNG assets used in documentation and presentation.

These files are part of the “museum wing” of the Estate, helping judges and readers understand the design.

---

## 3. Request Lifecycle (End‑to‑End)

1. **User selects a mode** in the Streamlit sidebar  
   e.g. *“Jeeves Remembers”* or *“Matters Requiring Investigation”*.

2. **User submits a prompt** in the chat input.  

3. `app.py` passes the prompt + mode to the orchestrator:  
   `WestmarchOrchestrator.run(workflow_name, user_input, selected_mode=...)`  

4. **Workflow selection & delegation**  
   - The orchestrator chooses a workflow (planning, research, critique, etc.).  
   - Jeeves frames the task and delegates to Perkins, Pennington, or Hawthorne as needed.  

5. **Agent work & tools**  
   - Agents call their configured LLM models.  
   - Perkins may simulate tool‑like behaviour (metadata scanners, structured reports).  
   - Pennington may call into the `MemoryBank` to save notes.  

6. **Memory interaction (when appropriate)**  
   - For normal flows, Pennington writes new entries with inferred tags.  
   - For recall flows (“Jeeves Remembers”), Jeeves invokes the memory recall pipeline to retrieve past events.  

7. **Response assembly**  
   - Jeeves collects agent outputs, summarises them in character, and returns final text to the UI.  

8. **Display**  
   - The chat transcript is updated with both user and staff messages, preserving avatars and roles.

---

## 4. Memory & Tagging Architecture (Summary)

Full details live in `docs/memory.md`; this section provides a concise architectural view.

### 4.1 Writing to Memory

- Miss Pennington’s helper method (e.g. `save_note(...)`) constructs entries with:
  - `timestamp` (ISO)  
  - `content` (human‑readable text)  
  - `tags` (list of strings)  

- Tag pipeline:
  1. Infer domains from the **user input** and sometimes the content.  
  2. Add tags such as `domain:finance`, `domain:poetry`, `domain:gnome`.  
  3. Add workflow‑specific tags like `type:parlour`, `type:planning`, `type:critique`.  
  4. Prepend `"auto"` as a generic tag for automated records.  

- Entries are appended to `memory.json` via `MemoryBank`, with logging like:
  - `MEMORY: Saving note (86 words)`  
  - `MEMORY: Saving file with 52 entries`  

### 4.2 Domain Inference (`tagging.py`)

- Maintains a `DOMAIN_KEYWORDS` map:
  - `poetry` → `["poem", "poetry", "verse", "languid moon", ...]`  
  - `finance` → `["market", "etf", "portfolio", "stock", ...]`  
  - `gnome` → `["gnome", "garden gnome", "barnaby", ...]`  
  - etc.

- `infer_domains(text: str) -> set[str]`:
  - Lowercases text, performs simple tokenisation.  
  - Uses whole‑word matching for single tokens and substring matching for key phrases.  
  - Returns a set of high‑level domains, e.g. `{"poetry", "critique"}`.

This function is used both when **writing** memory (to set tags) and when **reading** memory (to evaluate domain coherence).

### 4.3 Recall Pipeline (`Jeeves Remembers`)

When the user selects **“Jeeves Remembers”** and asks a recall question:

1. Jeeves first checks for **closure phrases**  
   (e.g. “Thank you, that will be all”) and exits early if detected.

2. Otherwise, the system:
   - Extracts hints and keywords from the query.  
   - Loads all memory entries via `MemoryBank.load_all()`.  
   - Scores each entry based on:
     - Keyword overlap  
     - Agent/subject hints  
     - Tag/domain alignment  

3. Logs top candidates:
   ```text
   MEMORY-RECALL: Highest scoring entry achieves → 5
   MEMORY-RECALL: Showing top 10 candidates by score:
   MEMORY-RECALL: • score  5 → Critique requested from Lady Hawthorne: ...
   ```

4. Computes `user_domains` from the query and `entry_domains` from tags/content.  

5. Selects a **domain‑coherent** candidate when possible:
   - If `user_domains ∩ entry_domains` is non‑empty, favour that entry.  
   - Otherwise, fall back to the best overall score.  

6. Jeeves returns the chosen entry, wrapped in an in‑character response such as:
   > “Indeed, sir. Upon consulting Miss Pennington’s carefully kept ledger, I find the following relevant recollection…”

This setup gives the Estate a small but convincing long‑term memory — inspectable, debuggable, and theatrically framed.

---

## 5. Demos & Scenarios

The architecture is illustrated through **nine in‑universe demos** in:

```text
westmarch/demos_in_universe/
```

- Demos 1–8: manually reenacted via the UI using scripted `.md` files.  
- **Demo 9 – A Mystery in the Archives**:  
  - Fully automated, triggered from the `Matters Requiring the Whole Household` mode.  
  - Exercises:
    - Multi‑agent orchestration  
    - Parallel and sequential reasoning  
    - Critique loops  
    - Memory‑aware narration and logging  

These scenarios double as **integration tests** of the architecture and as an in‑universe tour for judges.

---

## 6. Non‑Technical Flourishes

The same system could have been presented as a bare “agent framework”.  
Instead, Westmarch layers on:

- Distinct, well‑grounded **personas** with voices and roles.  
- **Narrative naming** of modes and workflows (“Arrangements for the Day”, “Jeeves Remembers”).  
- **Gamified, humorous framing** that remains genuinely useful for planning, drafting, research, and critique.  

Architecturally, however, the Estate remains:

- Modular  
- Inspectable  
- Extensible  

Beneath the wallpaper, it is a clean, multi‑agent, memory‑aware system.  
Above it, one finds a butler, a valet, a secretary, and a critic — all at your service.
