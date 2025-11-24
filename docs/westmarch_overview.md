# Westmarch House — System Overview
A Technical Account by Jeeves, Head of Household Operations

## 1. Introduction
Westmarch House is a multi-agent orchestration system designed to simulate a refined domestic staff—each agent possessing a defined role, operational domain, and stylistic persona. The architecture emphasizes modularity, clarity of responsibility, and fluid coordination among agents.

This overview provides a technical description of the system’s structure and key design principles.

---

## 2. System Architecture

### 2.1 High-Level Layout
The system is composed of four primary agents:

- **Jeeves** — Orchestrator, primary conversational interface, executive controller  
- **Perkins** — Research Footman: factual investigation, structured analysis  
- **Miss Pennington** — Scribe & Archivist: drafting, summarization, long-term memory  
- **Lady Hawthorne** — Critic: literary critique, rhetorical polishing, stylistic refinement  

All agents interact through a central orchestrator class:  
`WestmarchOrchestrator`.

### 2.2 Data Flow
1. **User Input** → received by Streamlit UI  
2. **Jeeves** → interprets intent and selects workflow  
3. **Workflow Method** (e.g., `plan_day`, `parlour_discussion`, `recall_memory`)  
4. **Supporting Agents** act as required  
5. **Miss Pennington** archives long-term records  
6. **Final Response** returned to the UI

---

## 3. Key Features

### 3.1 Orchestrated Multi-Agent Workflows
Each use case is implemented as a workflow in the orchestrator.  
Examples:
- Parlour conversations  
- Daily planning  
- Research tasks  
- Drafting and correspondence  
- Multi-agent gnome investigation  
- Memory recall (“Jeeves Remembers”)

### 3.2 Persona-Bound Styling
Responses are signature-consistent:
- Jeeves: courteous, succinct, steady  
- Perkins: analytical and structured  
- Miss Pennington: elegant and precise  
- Lady Hawthorne: incisive, barbed, and witty  

Consistency is enforced through prompts and workflow constraints.

---

## 4. Text-Based Architecture Diagram
```
            ┌────────────────────────────┐
            │     Streamlit Interface    │
            └──────────────┬─────────────┘
                           │
                           ▼
                          🎩
                 ┌──────────────────┐
                 │      Jeeves      │
                 │ Orchestrator API │
                 └─────────┬────────┘
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
    📚                    ✒️                    🕯️
┌──────────────┐   ┌────────────-──┐   ┌───────────────--──┐
│   Perkins    │   │  Pennington   │   │ Lady Hawthorne    │
│   Research   │   │   Drafting    │   │ Critique Engine   │
└───────┬──────┘   │ Memory Store  │   └──────────────-──-─┘
        │          └───────┬────-──┘
        │                  │
        │                  ▼
        │        ┌───────────────--──┐
        │        │    memory.json    │
        │        │  Long-Term Store  │
        │        └───────────────────┘
        ▼
User receives final polished result
```
---

## 5. Memory System Overview

### 5.1 Storage
Long-term memory is managed by Miss Pennington:

- Stored in `memory.json`
- Each entry contains:
  - timestamp  
  - content  
  - tags (optional)  
  - type (optional)  

### 5.2 Retrieval
The “Jeeves Remembers” workflow performs:
- keyword extraction  
- candidate scoring  
- domain inference  
- strict domain prioritization  
- graceful fallback  

This produces accurate recall even for vague user queries.

---

## 6. Extensibility
The system is designed for easy augmentation:
- new agents  
- new workflows  
- custom domains  
- additional memory strategies  
- external knowledge bases  

The orchestrator acts as a stable coordinating interface, allowing expansion without modifying existing agents.

---

## 7. Conclusion
Westmarch House provides a robust model for multi-agent orchestration with a strong stylistic identity, clean separation of responsibilities, and modular extensibility. This overview serves as a foundation for understanding the architecture and guiding future enhancements.