# The House of Westmarch — Architectural Overview

This document describes how the Estate is constructed behind the scenes.

---

## High-Level Diagram (Verbal)

User 👤 interacts via **Streamlit UI** in `app.py` →  
Request sent to **Jeeves** 🎩 (orchestrator) →  
Jeeves decides which staff member should handle the task →  

- Research tasks → 📚 Perkins  
- Drafting / summarisation → ✒️ Miss Pennington  
- Critique / evaluation → 🕯️ Lady Hawthorne  
- Planning / coordination → 🎩 Jeeves himself  

Agents may in turn call tools or other agents.  
Results are returned to Jeeves, who summarises and responds to the user.

Memory is recorded in `westmarch/data/memory.json`.

---

## Packages

### 1. `westmarch/agents/`

- `base_agent.py` — shared logic for all staff.  
- `jeeves.py` — orchestration agent; also functions as a direct conversational partner.  
- `perkins.py` — research agent; routes to search/tool functions.  
- `miss_pennington.py` — drafting/summarisation agent.  
- `lady_hawthorne.py` — critique agent.  
- `personas.md` — description of personas and system prompts.

Each file defines:

- an instruction prompt (persona),  
- any tools that agent may use,  
- and helper functions for orchestration.

---

### 2. `westmarch/core/`

- `models.py`  
  - Contains helpers for creating Gemini model clients and configuration.  

- `memory.py`  
  - In-memory plus JSON-backed persistence.  
  - Stores conversation turns, summaries, and key decisions.  
  - Provides retrieval and compaction utilities.  

- `messages.py`  
  - Internal message and role abstractions.  
  - Standardises communication between agents and orchestrator.  

- `logging.py`  
  - Sets up logging for debugging and tracing.  

---

### 3. `westmarch/orchestrator/`

- `router.py`  
  - Takes a user intent and selects a primary workflow.  
  - Encodes “Parlour Discussions”, “Arrangements for the Day”, etc.  

- `workflows.py`  
  - Multi-step routines: e.g. research → drafting → critique.  
  - Encapsulates more complex flows for demo scenarios.

---

### 4. `westmarch/data/`

- `memory.json`  
  - Simple JSON storage of summarised conversations.  
  - Used for “What did I tell you yesterday?” style queries.

---

### 5. Front-End: `app.py`

A Streamlit application:

- Sidebar: “The House of Westmarch – The Estate’s Available Services”.  
- Main panel: chat interface between 👤 and the staff.  
- Handles avatars: 👤, 🎩, 📚, ✒️, 🕯️, 🏰.  
- Routes UI actions into orchestrator workflows.

---

## Non-Technical Flourishes

The same architecture could be presented in purely technical terms.  
Instead, Westmarch introduces:

- **Persona grounding** via rich prompts and avatars.  
- **Narrative naming** of flows (“Arrangements for the Day” instead of “/plan”).  
- **In-universe demos** documenting behaviour as stories rather than raw logs.

These do not alter the core architecture, but they radically improve *user experience* and memorability.

---

In short:  
Beneath the wallpaper, Westmarch is a clean, modular, multi-agent system.  
Above it, one finds a butler, a valet, a secretary, and a critic.