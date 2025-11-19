# Memory System Overview

**House of Westmarch — Multi-Agent Application**  
*(Technical Documentation)*

The House of Westmarch employs a lightweight long-term memory system to preserve meaningful interactions, project continuity, and agent-relevant context.

---

## 1. Architecture (High-Level)

ASCII-safe diagram:

User Message  
     |  
     v  
Orchestrator (router.py -> workflows.py)  
     |  
     +--> Event Processor (messages.py)  
     |  
     +--> Memory Manager (memory.py)  
     |         - load memory (startup)  
     |         - write memory (triggered events)  
     |         - retrieve memory (context building)  
     |  
     +--> Agents (jeeves, perkins, pennington, hawthorne)  
               (memory optionally embedded into prompts)

---

## 2. Memory Storage Location

Memory is stored persistently in:

```
westmarch/data/memory.json
```

---

## 3. Which Events Are Archived

### Archived Events

| Event Type            | Description |
|-----------------------|-------------|
| user_fact            | User preferences & background details |
| user_intent          | User plans, intentions |
| project_update       | Updates about House tasks or creative projects |
| artifact_result      | Generated agent output (drafts, poems, summaries) |
| agent_feedback       | Critiques or evaluations |
| memory_query_answer  | Answers to recall-based questions |
| notable_event        | Any meaningful event worth remembering |

### Not Archived

| Event Type     | Reason |
|----------------|--------|
| Greetings      | Too trivial |
| Ephemeral text | No long-term value |
| Debug logs     | Technical only |

---

## 4. Triggering Events for Memory Creation

- User expresses preferences  
- User begins or continues a task or project  
- Agents produce substantial work  
- User explicitly requests remembering  
- User asks recall-style questions  
- Multi-agent workflows reach meaningful checkpoints  

---

## 5. How Memory Is Accessed

Memory retrieval uses:

```
memory.search(query)
memory.recent(n)
memory.filter_by_type(type)
```

Triggered when:

- User asks recall-based questions  
- Agents require prior context  
- Multi-step tasks resume  
- Jeeves performs planning duties  

---

## 6. Agents With Memory Access

| Agent              | Uses Memory? | Purpose |
|--------------------|--------------|---------|
| Jeeves             | Yes          | Planning, continuity |
| Perkins            | Yes          | Research context |
| Miss Pennington    | Yes          | Drafting continuity |
| Lady Hawthorne     | Yes          | Critique continuity |
| Orchestrator       | Always       | Context assembly |

---

## 7. Example Memory Flow

Example (ASCII-safe):

User -> "Jeeves, continue my poem from yesterday."  
      |  
      v  
Orchestrator determines memory is required  
      |  
      +--> memory.search("poem")  
      |       returns:  
      |         - Hawthorne critique  
      |         - Pennington revision notes  
      |         - User's intended themes  
      |  
      v  
Jeeves receives context bundle  
      v  
Jeeves generates continuation consistent with prior context  

---

## Summary

| Function | Mechanism |
|----------|-----------|
| Storage | JSON file (`westmarch/data/memory.json`) |
| Triggers | Intent, preferences, artifacts, critiques |
| Access | Context creation, recall, planning |
| Agents | All agents + orchestrator |
| Purpose | Continuity, personalization, project coherence |
