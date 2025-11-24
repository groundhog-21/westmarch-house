# Westmarch House — System Architecture
A Formal Technical Description

## 1. Objective
This document presents a strict technical account of the system’s architecture—the structural components, agent roles, workflow design, and data pathways constituting the Westmarch House multi-agent application.

---

## 2. Component Summary

### 2.1 Orchestrator
`WestmarchOrchestrator` serves as the central controller:
- interprets user intent  
- delegates tasks  
- coordinates inter-agent collaboration  
- performs memory lookup  
- manages workflow context  

It exposes a suite of workflow methods corresponding to use cases.

### 2.2 Agents
Each agent is a prompt-specialized LLM wrapper with an explicit domain.

| Agent | Role | Core Functions |
|-------|------|----------------|
| **Jeeves** | Executive orchestrator | Conversational interface, workflow routing, final presentation |
| **Perkins** | Research Footman | Structured investigation, data analysis |
| **Miss Pennington** | Archivist & Scribe | Drafting, summarization, long-term memory management |
| **Lady Hawthorne** | Critique Engine | Editorial critique, stylistic transformation |

All agents communicate only through the orchestrator.

---

## 3. Workflows

### 3.1 Workflow Structure
A workflow typically follows:
1. extract user intent  
2. run closure detection  
3. prepare context  
4. call necessary agent(s)  
5. archive results  
6. return polished output  

### 3.2 High-Level Workflow Listing
- **Parlour Discussions**  
- **Arrangements for the Day**  
- **Matters Requiring Investigation**  
- **Correspondence & Drafting**  
- **Archive Summary Retrieval**  
- **Her Ladyship’s Critique**  
- **Multi-Agent Orchestration Demo**  
- **Memory Recall (“Jeeves Remembers”)**  
- **Mystery in the Archives (Surprise Demo)**  

Each workflow is deterministic in structure and persona-consistent in output.

---

## 4. Memory Recall System

### 4.1 Scoring
Each memory entry is scored along:
- keyword matches  
- number of matches  
- contextual similarity  

Top candidates are then passed to domain filters.

### 4.2 Domain Inference
A static dictionary maps keywords → semantic domains.  
This prevents inappropriate cross-domain retrieval (e.g., poetry returned for a finance query).

### 4.3 Strict Domain Prioritization
If user query suggests domain(s):
- remove candidates not matching at least one inferred domain  
- fallback to keyword matches only if necessary  
- fallback to “no recollection” if no domain-coherent matches exist  

---

## 5. Storage

### 5.1 `memory.json`
A robust append-only log where each entry represents:
- parlour remarks  
- drafts  
- research results  
- critiques  
- workflow summaries  

Miss Pennington manages insertion.  
Jeeves performs retrieval.

---

## 6. Diagrammatic Summary
```
                     🎩
┌──────────────────────────────────────────────┐
│                  Jeeves                      │
│----------------------------------------------│
│ Routes tasks • Applies workflows • Evaluates │
│ memory • Coordinates agents                  │
└────────────┬───────────────┬─────────────────┘
             │               │
             │               │      
             ▼               ▼
            📚              ✒️
     ┌────────────-──┐   ┌──────────-──┐
     │   Perkins     │   │ Pennington  │
     │   Research    │   │ Drafting &  │
     └───────┬───────┘   │   Memory    │
             │           └──────┬──────┘
             │                  │
             │                  ▼
             │             memory.json
             ▼
            🕯️
     ┌─────────----────┐
     │  Lady Hawthorne │
     │  Critique       │
     └───────────---───┘
```
---

## 7. Summary
This document captures the complete architectural specification of Westmarch House. It establishes the system's modular, persona-bound, workflow-driven structure and provides a foundation for maintenance and future development.