# 📚 Memory System Overview (Updated & Expanded)
### House of Westmarch — Technical Documentation

The House of Westmarch includes a structured, domain-aware, JSON-backed memory system that supports continuity, recall, and multi-agent context-building across sessions and demos.

This document describes the **current** architecture, features, retrieval logic, and memory-aware agent workflows.

---

## 1. High-Level Architecture

```
USER MESSAGE
     │
     ▼
🧭 ORCHESTRATOR  (router.py → workflows.py)
     │
     ├── Normalised Event Processing  (messages.py)
     │
     ├── Memory Manager               (memory.py)
     │     • load_all()
     │     • save_entry()
     │     • search()
     │     • domain inference
     │     • text conversion
     │
     └── Agents (Jeeves, Perkins, Miss Pennington, Lady Hawthorne)
           • Prompts may include retrieved memory context
           • Pennington writes new entries
```

Memory is stored persistently at:

```text
westmarch/data/memory.json
```

---

## 2. Persistent Memory Storage

### File Format

Each entry is a JSON object of the form:

```json
{
  "timestamp": "2025-11-26T13:45:10.123Z",
  "content": "Parlour discussion entry: ...",
  "tags": ["parlour", "jeeves", "gnome"]
}
```

Entries are created exclusively via the `MemoryBank` class in `memory.py`.

Miss Pennington acts as the **house archivist**, responsible for saving:

- Parlour logs  
- Discrepancy Reports  
- Research notes  
- Summaries  
- Project updates  
- Notable events  

---

## 3. Memory Event Types

### Archived Event Types

| Event Type            | Description                                   |
|-----------------------|-----------------------------------------------|
| `parlour_log`         | User ↔ Jeeves conversational turns           |
| `discrepancy_report`  | Pennington’s archival findings               |
| `research_summary`    | Perkins’s structured analyses                |
| `critique_entry`      | Hawthorne’s evaluations                      |
| `artifact_result`     | Poems, drafts, letters, summaries            |
| `notable_event`       | Any memorable estate incident                |
| `memory_query_answer` | Jeeves’ responses to recall-style questions  |
| `user_fact`           | User preferences, background details         |
| `user_intent`         | User plans or stated goals                   |

### Not Archived

| Event Type       | Reason                    |
|------------------|---------------------------|
| Greetings        | Too trivial               |
| Ephemeral filler | No long-term value        |
| Debug logs       | Technical, internal only  |

---

## 4. Memory Writing: How Entries Are Created

Miss Pennington saves notes through methods like:

```python
self.pennington.save_note(
    "Parlour discussion entry:\n\n"
    f"USER SAID:\n{user_input}\n\n"
    f"JEEVES REPLIED:\n{jeeves_reply}"
)
```

All writes:

- Use `_load()` / `_save()` for JSON safety  
- Add an ISO timestamp  
- Attach optional tags  
- Emit logging messages such as:

```text
MEMORY: Saving note (42 words)
MEMORY: Loaded 17 notes
MEMORY: Saving file with 18 entries
```

Typical triggers for memory creation:

- User engages in a Parlour discussion  
- Pennington drafts or updates a Discrepancy Report  
- Perkins completes a research summary  
- Hawthorne issues a substantive critique  
- A multi-agent workflow reaches a meaningful conclusion  

---

## 5. Modern Memory Retrieval Pipeline (Jeeves Remembers)

The **Jeeves Remembers** feature implements a structured recall workflow.

### 5.1 Closure Detection

If the user input contains phrases like:

> “That will be all”, “Thank you”, “That will suffice”

Jeeves returns a short closing line and **skips** the recall pipeline.

---

### 5.2 Hint Extraction

```python
_extract_memory_hints(user_input: str) -> Dict[str, List[str]]
```

Extracts:

- `keywords` (e.g. `poem`, `gnome`, `plan`, `letter`, `critique`)  
- `agent_hints` (mentions of Jeeves, Pennington, Perkins, Lady Hawthorne)  
- `topic_hints` (e.g. poetry, planning, letter-writing)  
- `time_hints` (`yesterday`, `earlier today`, `last week`)  

Hints are deduplicated and stored in a lightweight dictionary.

---

### 5.3 Loading Candidates

```python
all_notes = pennington.load_all_notes()
```

Logs:

```text
MEMORY: Loading all notes
MEMORY: Loaded N notes
```

All notes are considered candidates for scoring.

---

### 5.4 Scoring Candidates

Two layers of scoring are used:

1. **Keyword overlap scoring**  
   - Count of query tokens that appear in each entry’s content.  

2. **Hint-based scoring** (when using `_find_best_memory_match`)  
   - `+3` for strong keyword matches  
   - `+2` for agent name matches  
   - `+1` for weaker topic hints  

Entries with zero score are discarded.

---

### 5.5 Top-10 Candidate Logging

The best candidates are sorted by score (descending), and only the **top 10** are logged:

```text
MEMORY-RECALL: Highest scoring entry achieves → 5
MEMORY-RECALL: Showing top 10 candidates by score:
MEMORY-RECALL: • score  5 → [2025-…] Pennington: Discrepancy Report…
MEMORY-RECALL: • score  4 → [2025-…] Perkins: Metadata notes…
```

Snippets are truncated for readability.

---

### 5.6 Domain Inference (New)

`memory.py` defines a `DOMAIN_KEYWORDS` mapping, including domains such as:

- `poetry`  
- `finance`  
- `gnome`  
- `weather`  
- `schedule`  
- `drafting`  
- `research`  
- `history`  
- `parlour`  
- `critique`  
- `sports`  

`infer_domains(text: str)`:

- Normalises text to lowercase  
- Handles multi-word phrases (e.g. `"garden gnome"`) by substring match  
- Uses whole-word token matching for single words  

Domain sets are computed for:

- The user query  
- Each candidate memory entry  

**Selection rule:**

- If `user_domains` is non-empty, prefer entries where  
  `user_domains ∩ entry_domains` is not empty.  
- If no such entries exist among the top 10, fall back to the single best-scoring entry overall.

---

### 5.7 Fallback Rules

If no candidates survive domain coherence filtering:

- The highest-scoring entry from the top 10 is used.  

If there are no candidates at all:

- Jeeves replies that no suitable recollection could be found and invites the user to provide more detail.

---

### 5.8 Final Jeeves Reply

Once a `chosen_entry` is selected:

- Its `content` is inserted into a templated Jeeves response, e.g.:

> “Indeed, sir. Upon consulting Miss Pennington’s carefully kept ledger,  
> I find the following relevant recollection: …”

The tone is:

- Calm  
- Deferential  
- Ready to perform further searches if requested  

---

## 6. Agent Access Levels

| Agent               | Access Type | Purpose                                  |
|---------------------|------------|------------------------------------------|
| **Jeeves**          | Read       | Recall, planning, continuity             |
| **Perkins**         | Read (via prompts) | Research context, anomaly history |
| **Miss Pennington** | Write      | Logs, reports, archival notes            |
| **Lady Hawthorne**  | Read (via prompts) | Critique continuity             |
| **Orchestrator**    | Indirect   | Builds contexts that may include memory  |

In practice:

- Pennington **writes** memory.  
- Jeeves **reads and interprets** memory in `recall_memory`.  
- Other agents may receive memory snippets embedded into their system or user prompts as needed.

---

## 7. Domain Inference System

Located in `memory.py` as `DOMAIN_KEYWORDS` and `infer_domains`.

Characteristics:

- Supports both single-word and multi-word keys  
- Uses token-based matching for robustness  
- Returns a `set[str]` of high-level domains for any given text  

Used primarily for:

- Disambiguating recall queries  
- Ensuring that poetry questions fetch poetry-related memory, etc.  
- Supporting more precise behaviour in Demo 8 (“Jeeves Remembers”) and related flows.

---

## 8. Example: Updated Recall Flow

```text
User: "Jeeves, what did Lady Hawthorne say about my poem yesterday?"
```

1. **Hint extraction**

   ```text
   keywords    → ["poem", "languid moon"]
   agent_hints → ["lady hawthorne"]
   topic_hints → ["poem"]
   time_hints  → ["yesterday"]
   ```

2. **Load notes**

   ```text
   MEMORY: Loading all notes
   MEMORY: Loaded N notes
   ```

3. **Score & rank candidates**

   - Overlap with `"poem"`, `"languid moon"`, `"lady hawthorne"`  
   - Top 10 logged

4. **Infer domains**

   ```text
   user_domains   → {"poetry", "critique"}
   entry_domains  → e.g. {"poetry", "critique"}
   ```

5. **Select best domain-coherent candidate**

6. **Jeeves replies** with the chosen entry’s content, framed as a recollection from Miss Pennington’s ledger.

---

## 9. Summary of the Modern Memory System

| Feature                              | Status          |
|--------------------------------------|-----------------|
| JSON-based persistent store          | ✔ Implemented   |
| Timestamped entries with tags        | ✔ Implemented   |
| Keyword + tag search                 | ✔ Implemented   |
| Weighted recall scoring              | ✔ Implemented   |
| Domain inference for coherence       | ✔ Implemented   |
| Top-10 candidate logging             | ✔ Implemented   |
| Closure phrase detection             | ✔ Implemented   |
| Pennington as archivist              | ✔ Implemented   |
| Jeeves Remembers workflow            | ✔ Implemented   |
| Use in demos (especially Demo 8)     | ✔ Implemented   |


The result is a **lightweight but capable memory layer**:  
simple enough to inspect (a single JSON file), yet powerful enough to support narrative recall, continuity, and domain-aware responses throughout the House of Westmarch.