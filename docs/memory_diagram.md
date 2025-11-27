                 👤 USER
                     │
                     ▼
            🏰 Streamlit UI (app)
                     │
                     ▼
           🎩 JEEVES — Orchestrator
                     │
      (recall workflow triggers memory search)
                     │
                     ▼
          🧠 MEMORY MANAGER (MemoryBank)
       ┌───────────────────────────────────┐
       │ • load_all()                      │
       │ • search(query)                   │
       │ • save_entry(content, tags)       │
       │ • JSON store (memory.json)        │
       │ • logging on load/save/search     │
       └───────────────────────────────────┘
                     ▲
                     │   (writes new entries)
                     │
           ✒️ MISS PENNINGTON — Archivist
       ┌───────────────────────────────────┐
       │ • save_note()                     │
       │ • archives user–agent exchanges   │
       │ • maintains the household ledger  │
       └───────────────────────────────────┘
                     │
                     ▼
       (Jeeves retrieves notes during recall)
                     │
                     ▼
          🎩 JEEVES — Memory Recall Engine
       ┌───────────────────────────────────┐
       │ • extract hints (keywords/agents) │
       │ • score entries by keyword match  │
       │ • domain coherence filtering      │
       │ • select best matching note       │
       └───────────────────────────────────┘
                     │
                     ▼
              Final reply to user