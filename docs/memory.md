# 📚 **Memory System Overview**

**House of Westmarch --- Technical Documentation**\
**Updated: December 2, 2025**

The House of Westmarch includes a structured, domain-aware, JSON-backed
memory system that supports continuity, recall, and multi-agent
context-building across sessions and demonstrations.

This document describes the current architecture, features, retrieval
logic, tagging system, and memory-aware agent workflows.

------------------------------------------------------------------------
```
# 1. High-Level Architecture

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
         │     • JSON-backed persistent store
         │     • delegates domain/tag inference to tagging.py
         │
         ├── Tagging System (tagging.py)
         │     • infer_tags_from_user_input()
         │     • infer_domains()
         │     • DOMAIN_KEYWORDS registry
         │     • standardised namespaces: domain:*, type:*, auto
         │
         └── Agents (Jeeves, Perkins, Miss Pennington, Lady Hawthorne)
               • Agents may receive memory-infused prompts
               • Miss Pennington writes new memory entries
```
Memory is stored persistently at:

    westmarch/data/memory.json

------------------------------------------------------------------------

# 2. Persistent Memory Storage

Each entry is a JSON object of the form:

``` json
{
  "timestamp": "2025-12-01T19:28:39.642244",
  "content": "Parlour discussion entry: ...",
  "tags": ["auto", "domain:gnome", "type:parlour"]
}
```

### Key Principles

-   **Every entry begins with `auto`.**
-   **All tags are derived strictly from user input**, never generated
    output.
-   Domains appear as: `domain:poetry`, `domain:finance`,
    `domain:gnome`, etc.
-   Event/workflow types appear as: `type:parlour`, `type:critique`,
    `type:planning`.
-   Orchestrators may add workflow-specific tags (e.g.,
    `"type:parlour"`).

Entries are created exclusively through `MemoryBank` in `memory.py`,
with Miss Pennington serving as the house archivist.

------------------------------------------------------------------------

# 3. Memory Event Types (as Tags)

With the modern system, "event types" are expressed directly as tags:
```
  -----------------------------------------------------------------------
  Tag Prefix                                    Meaning
  --------------------------------------------- -------------------------
  `type:*`                                      Workflow type (parlour,
                                                planning, critique,
                                                whole-household...)

  `domain:*`                                    Topic classification
                                                (poetry, finance, gnome,
                                                schedule...)

  `auto`                                        Always included; marks
                                                automatically generated
                                                tags
  -----------------------------------------------------------------------
```
### Typical Saved Events

-   **type:parlour** --- Parlour conversations with Jeeves\
-   **type:critique** --- Lady Hawthorne's critiques\
-   **type:drafting** --- Pennington's drafting work\
-   **type:research** --- Perkins's investigations\
-   **type:whole-household** --- Multi-agent workflows\
-   **type:planning** --- Daily plans drafted by Jeeves

### Not archived

Some event types are deliberately excluded:

-   greetings\
-   trivial interactions\
-   filler text\
-   debug logs

------------------------------------------------------------------------

# 4. Memory Writing: How Entries Are Created

Miss Pennington performs all archival writes through:

``` python
self.pennington.save_note(content, extra_tags=...)
```

This pipeline guarantees:

-   safe load → modify → save with `_load()` / `_save()`
-   automatic timestamp insertion
-   tag inference from **user input only**
-   automatic insertion of `"auto"` tag
-   optional addition of workflow-level `type:*` tags

### Tagging Behaviour (Updated)

Provided by `tagging.py`:

-   `infer_tags_from_user_input(text)`\
-   `infer_domains(text)`\
-   tags include:
    -   `domain:*`
    -   `type:*` (only when appropriate)
    -   `auto` (always first)
-   agents' output is never used for tag inference

### Typical Save Triggers

-   Parlour discussions\
-   Planning workflows\
-   Research notes\
-   Pennington's summaries\
-   Critique responses\
-   Whole-household operations\
-   Memory approvals ("This will do nicely.")

Logging example:

    MEMORY: Saving note (86 words)
    MEMORY: Loaded 52 notes
    MEMORY: Saving file with 53 entries
    MEMORY: Save complete

------------------------------------------------------------------------

# 5. Modern Memory Retrieval Pipeline ("Jeeves Remembers")

`recall_memory()` implements a structured metadata-aware recall process.

------------------------------------------------------------------------

## 5.1 Closure Detection

If the user input contains phrases such as:

-   "Thank you"
-   "That will be all"
-   "That will suffice"

Then the memory recall flow is aborted and Jeeves responds politely.

------------------------------------------------------------------------

## 5.2 Domain Extraction (New --- via tagging.py)

Domains are inferred strictly through `infer_domains(text)`:

-   Normalizes to lowercase\
-   Matches both single-word and multi-word phrases\
-   Returns canonical domain identifiers

Example:

    infer_domains("What did we learn about the gnome yesterday?")
    → {"gnome"}

If the user query yields **no domains**, the recall mechanism uses
scoring alone.

------------------------------------------------------------------------

## 5.3 Loading Candidates

All entries are loaded:

    all_notes = pennington.load_all_notes()

Logged in Streamlit:

    MEMORY: Loading all notes
    MEMORY: Loaded 58 notes

All notes are considered candidates for scoring.

------------------------------------------------------------------------

## 5.4 Candidate Scoring (Updated)

A single scoring rule is used:

    score = number of user query tokens appearing in entry.content.lower()

Notes with score 0 are discarded.

------------------------------------------------------------------------

## 5.5 Top-10 Candidate Logging

Candidates are sorted by decreasing score. Only the top 10 are logged:

    MEMORY-RECALL: Highest scoring entry achieves → 5
    MEMORY-RECALL: Showing top 10 candidates:
    • score  5 → [Whole Household Workflow Summary] USER REQUEST: …
    • score  4 → Critique requested from …
    ...

------------------------------------------------------------------------

## 5.6 Domain Filtering Using Tags (New)

For each entry in the top 10:

1.  Extract its domain set:
    -   only from **tags**, not content\
    -   e.g. `["auto", "domain:gnome", "type:whole-household"]` →
        `{"gnome"}`
2.  Apply domain filtering:

-   If **user_domains** is **non-empty**:
    -   choose the **first entry** whose domain set intersects the
        user's domains\
-   If none match:
    -   fall back to the **highest-scoring** entry

If **user_domains** is empty: - skip domain filtering entirely\
- choose the highest scoring entry

This behaviour matches the real logs from Dec 2 tests.

------------------------------------------------------------------------

## 5.7 Fallback Rules

-   If no entries survive scoring (rare):\
    Jeeves apologizes and invites a more detailed query.

-   If no domain-coherent entry exists among the top 10:\
    The top-scoring entry is returned.

------------------------------------------------------------------------

## 5.8 Final Jeeves Reply

Once a `chosen_entry` is selected, Jeeves replies:

> "Indeed, sir. Upon consulting Miss Pennington's carefully kept
> ledger,\
> I find the following relevant recollection:\
> ... (content) ...\
> Shall I search again?"

Tone properties:

-   polite\
-   deferential\
-   precise\
-   continuity-aware

------------------------------------------------------------------------

# 6. Agent Access Levels
```
  -------------------------------------------------------------------------
  Agent                             Read        Write         Notes
  --------------------------------- ----------- ------------- -------------
  **Jeeves**                        ✔           ✖             Reads for
                                                              recall,
                                                              planning
                                                              context

  **Perkins**                       ✔           ✖             May receive
                                                              memory for
                                                              research
                                                              continuity

  **Miss Pennington**               ✖           ✔             Sole writer
                                                              to persistent
                                                              memory

  **Lady Hawthorne**                ✔ (via      ✖             Continuity in
                                    prompt)                   critiques

  **Orchestrator**                  indirect    indirect      May include
                                                              memory
                                                              snippets in
                                                              system
                                                              prompts
  -------------------------------------------------------------------------
```
### Summary

-   **Pennington writes**\
-   **Jeeves reads**\
-   Others receive memory context indirectly through orchestrator
    construction

------------------------------------------------------------------------

# 7. Domain Inference System (tagging.py)

The domain inference logic lives in:

    westmarch/core/tagging.py

### Components

-   `DOMAIN_KEYWORDS` --- mapping of domain name → list of
    keywords/phrases\
    (e.g. `"poetry"`, `"finance"`, `"gnome"`, `"drafting"`,
    `"schedule"`, `"research"` ...)
-   `infer_domains(text)`\
-   `infer_tags_from_user_input(text)`

### Behaviour

-   Multi-word phrase matching (e.g., `"garden gnome"`)
-   Lowercase tokenization
-   Returns a `set[str]` such as:\
    `{"poetry"}`, `{"gnome"}`, `{"finance"}`

Used for:

-   filtering recall candidates\
-   generating `domain:*` tags during memory writes