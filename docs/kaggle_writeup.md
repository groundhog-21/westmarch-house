# 🏰 The House of Westmarch
### *A Fully Staffed, Mildly Unhinged Multi-Agent Concierge*
🎩 Jeeves · 📚 Perkins · ✒️ Miss Pennington · 🕯️ Lady Hawthorne · 👤 The Master

---

## Project Description

**The House of Westmarch** is a narrative-driven multi-agent concierge system presented as an Edwardian household. It implements:

- Multi-agent orchestration  
- Hybrid LLM usage (Gemini + OpenAI)  
- Tool-assisted reasoning  
- A domain-aware memory system  
- Critique loops  
- A Streamlit UI  
- Nine theatrical demonstrations  

Users delegate tasks to household “staff,” who perform real, engineered workflows beneath the polished narrative.

---

## 1. Problem Statement

Users face constant cognitive friction in planning, researching, drafting, critiquing, and remembering prior context.

Westmarch reframes these tasks as responsibilities of a household staff:

- 🎩 **Jeeves** — orchestration, planning, memory  
- 📚 **Perkins** — structured research  
- ✒️ **Miss Pennington** — drafting and refinement  
- 🕯️ **Lady Hawthorne** — critique  

This reduces user cognitive load and turns multi-agent AI into a comfortable experience.

---

## 2. Solution Overview

Westmarch integrates:

- Multi-agent coordination  
- Hybrid Gemini + OpenAI model usage  
- Persistent memory with domain inference  
- Tool-assisted reasoning from Perkins  
- Polished drafting from Pennington  
- Critique loops from Lady Hawthorne  
- Structured workflows in an orchestrator  
- An interactive Streamlit interface  

---

## 3. Agent Roster

### 🎩 Jeeves — Butler & Orchestrator
Handles requests, chooses workflows, delegates tasks, manages memory, and frames final responses.

### 📚 Perkins — Valet of Scholarly Inquiry
Produces structured investigations, anomaly analyses, and research briefs.

### ✒️ Miss Pennington — Secretary & Correspondent
Transforms chaotic notes into polished writing and archives events in long-term memory.

### 🕯️ Lady Hawthorne — Critic-in-Residence
Powered by OpenAI. Delivers sharp, focused critique in ≤3 sentences.

---

## 4. Architecture Summary

### 4.1 Orchestration — `westmarch/orchestrator/`
- `router.py`: selects workflow  
- `workflows.py`: defines multi-step agent sequences  

### 4.2 Core Services — `westmarch/core/`
- `models.py`: Gemini + OpenAI clients  
- `memory.py`: session + long-term memory  
- `tagging.py`: domain inference & auto-tagging  
- `messages.py`: structured messages  
- `logging.py`: traceable workflow logs  

### 4.3 Agents — `westmarch/agents/`
Four personas inheriting from a shared base class.

### 4.4 Memory Layer — `westmarch/data/memory.json`
Keyword scoring, tag-based domain inference, top-10 candidate ranking.

### 4.5 Front-End — `app.py`
Eight modes mapping directly to workflows:
- Parlour Discussions  
- Arrangements for the Day  
- Matters Requiring Investigation  
- Correspondence & Drafting  
- Records from the Archive  
- Her Ladyship’s Critique  
- Matters Requiring the Whole Household  
- Jeeves Remembers  

---

## 5. Key Features

- Multi-agent delegation  
- Sequential + parallel workflows  
- Tool-augmented research  
- Long-term memory with domain inference  
- Critique cycle  
- Hybrid Gemini/OpenAI use  
- Strong observability  
- Interactive UI  

---

## 6. Demonstrations (1–9)

### Demo 1 — Parlour Discussions
Base persona interactions.

### Demo 2 — Arrangements for the Day
Daily planning.

### Demo 3 — Matters Requiring Investigation
Structured research (“teacup psychology”).

### Demo 4 — Correspondence & Drafting
Pennington rescues rough notes.

### Demo 5 — Records & Summaries
Jeeves produces a structured archival summary.

### Demo 6 — Her Ladyship’s Critique
Lady Hawthorne critiques “O Languid Moon of Yesteryear.”

### Demo 7 — Misbehaving Garden Gnome
Multi-agent orchestration and escalation.

### Demo 8 — Memory Demonstration
Jeeves retrieves prior events with domain-aware filtering.

### Demo 9 — A Mystery in the Archives
Flagship demo:
- looped analysis  
- metadata reasoning  
- critique escalation  
- hybrid model switching  
- cinematic narrative pacing  

---

## 7. Value & Impact

### Practical
- Reliable research  
- Structured planning  
- High-quality drafting  
- Useful critique  
- Memory-aware coherence  

### Experiential
- Personas reduce cognitive load  
- Household metaphor clarifies agent roles  
- Streamlit UI makes the system approachable  

---

## 8. Conclusion

The House of Westmarch is a complete, polished multi-agent system demonstrating memory, orchestration, critique, and hybrid reasoning across nine narrative demos.

🕯️ *Lady Hawthorne:* “If this does not satisfy the judges, nothing will.”