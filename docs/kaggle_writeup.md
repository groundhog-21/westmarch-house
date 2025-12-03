# 🏰 The House of Westmarch
### *A Fully Staffed, Mildly Unhinged Multi-Agent Concierge*
🎩 Jeeves · 📚 Perkins · ✒️ Miss Pennington · 🕯️ Lady Hawthorne · 👤 The Master

---

## Project Description

**The House of Westmarch** is a gamified, narrative-driven multi-agent concierge system disguised as an Edwardian household. Beneath the humor and theatrics lies a fully engineered agentic platform integrating:

- Multi-agent orchestration  
- Hybrid model usage (Gemini + OpenAI)  
- A domain-aware memory system  
- Tool-assisted reasoning  
- Critique loops  
- Structured workflows  
- A Streamlit UI  
- Nine theatrical demonstrations (1–9)  

Users delegate tasks to “household staff,” creating an immersive experience that is both technically robust and unexpectedly entertaining.

---

## 1. Problem Statement

Modern users constantly manage small but cognitively expensive tasks: planning, researching, drafting, critiquing, and remembering previous conversations. These responsibilities accumulate until the user effectively becomes their own secretary, researcher, editor, and archivist.

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
- Polished drafting (Pennington)  
- Critique loops (Hawthorne)  
- Workflow-based reasoning patterns  
- A polished, intuitive Streamlit front-end  

The UI offers eight selectable modes, each mapping to an orchestrated workflow—making the system approachable for non-technical users while maintaining technical depth for judges and reviewers.

---

## 3. Agent Roster

### 🎩 Jeeves — Butler & Orchestrator
The central conductor of the household.  
Jeeves interprets user requests, selects the correct workflow, delegates tasks to other agents, manages memory queries, and ensures all responses maintain impeccable tone and structure.

### 📚 Perkins — Valet of Scholarly Inquiry
A structured researcher.  
Perkins generates numbered analyses, logical chains of thought, and tool-assisted investigations. His outputs resemble short research briefs or technical memos.

### ✒️ Miss Pennington — Secretary & Correspondent
The Estate’s editor and archivist.  
She refines rough notes into polished prose, drafts letters and summaries, and writes all memory entries into long-term storage.

### 🕯️ Lady Hawthorne — Critic-in-Residence
Powered by OpenAI.  
She delivers sharp, elegant critique of poetry, prose, and agent-generated drafts—always in ≤3 sentences—balancing severity with theatrical flair.

---

## 4. Architecture Summary

### 4.1 Orchestration — `westmarch/orchestrator/`
- **`router.py`** selects the correct workflow based on user mode  
- **`workflows.py`** defines multi-step sequences, such as  
  *research → draft → critique*  

Workflows include branching, looping, and combined sequential/parallel reasoning patterns.

### 4.2 Core Services — `westmarch/core/`
- **`models.py`** configures Gemini & OpenAI clients  
- **`memory.py`** manages session + long-term memory  
- **`tagging.py`** performs domain inference and auto-tagging  
- **`messages.py`** defines message schemas  
- **`logging.py`** provides detailed workflow logs  

### 4.3 Agents — `westmarch/agents/`
All agents inherit a shared base class and are prompted with elaborate persona definitions to maintain consistent voice, tone, and boundaries.

### 4.4 Memory Layer — `westmarch/data/memory.json`
The memory system includes:

- Keyword scoring  
- Tag-based domain inference  
- Top-10 candidate ranking  
- Closure-phrase detection  
- Persona-aware recall  

This enables Jeeves to answer “What did I tell you yesterday…?” with theatrical confidence.

### 4.5 Front-End — `app.py`
A Streamlit interface presenting eight modes:

- Parlour Discussions  
- Arrangements for the Day  
- Matters Requiring Investigation  
- Correspondence & Drafting  
- Records from the Archive  
- Her Ladyship’s Critique  
- Matters Requiring the Whole Household  
- Jeeves Remembers  

Each mode triggers a matching workflow, with Demo 9 fully automated.

---

## 5. Key Features

- Multi-agent delegation  
- Sequential and parallel reasoning  
- Hybrid LLM usage (Gemini and OpenAI)  
- Long-term memory with domain-aware filtering  
- Critique loops  
- Tool-augmented research  
- Observability through structured logs  
- Narrative immersion via personas and theatrical demos  
- A polished, judge-friendly UI  

---

## 6. Demonstrations (1–9)  
Westmarch includes nine “in-universe” theatrical demonstrations.

### Demo 1 — Parlour Discussions
Casual conversation, staff introductions, and persona grounding.

### Demo 2 — Arrangements for the Day
Jeeves converts rough goals into structured daily planning.

### Demo 3 — Matters Requiring Investigation
Perkins performs structured analysis (“teacup psychology”), showcasing tool use and disciplined reasoning.

### Demo 4 — Correspondence & Drafting
Miss Pennington transforms chaotic notes into polished letters.

### Demo 5 — Records & Summaries
Jeeves produces formal archival summaries of prior disasters.

### Demo 6 — Her Ladyship’s Critique
A demonstration of Hawthorne’s incisive critique style applied to  
*“O Languid Moon of Yesteryear.”*

### Demo 7 — The Misbehaving Garden Gnome
A multi-agent choreography featuring escalation, recall, investigation, and critique.

### Demo 8 — Memory Demonstration
Jeeves retrieves prior events using keyword scoring and domain inference.

### Demo 9 — A Mystery in the Archives (Fully Automated)
The flagship demo.  
This narrative unfolds automatically with a single button press and includes:

- Looping research cycles  
- Metadata scrutiny  
- Multi-agent council  
- Parallel branches  
- Critique escalation  
- Hybrid model switching  
- Dramatic reveals  

It runs to completion without further user input.

---

## 7. Value & Impact

### Practical Value
- Simplifies planning  
- Improves writing quality  
- Structures research  
- Provides high-quality critique  
- Maintains long-term continuity  

### Experiential Value
- Humorous, gamified, theatrical  
- Reduces cognitive load  
- Characters clarify agent roles  
- Streamlit UI lowers friction  
- Immersive narrative encourages exploration  

Westmarch demonstrates that agentic systems can be:

- useful  
- comprehensible  
- delightful  

—without sacrificing technical depth.

As the staff observe:

- 🎩 Jeeves: “The Estate restores dignity to everyday tasks.”  
- ✒️ Pennington: “No more wrestling with blank pages.”  
- 📚 Perkins: “Clarity is but a request away.”  
- 🕯️ Hawthorne: “And the prose improves.”  

---

## 8. Conclusion

**The House of Westmarch** is a complete, humorous, and immersive multi-agent concierge system. It blends theatrical presentation with serious engineering: tool use, memory, criticism, planning, and multi-step orchestration across two LLM platforms.

Its Streamlit interface and nine demos offer reviewers an intuitive, interactive tour through the Estate’s capabilities.

🕯️ *Lady Hawthorne:*  
“If this does not satisfy the judges, nothing will.”