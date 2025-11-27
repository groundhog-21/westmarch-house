from westmarch.core.memory import MemoryBank

# Use the same path Pennington uses, so we test the real file
path = "westmarch/data/memory.json"

print("\n=== MEMORY LOGGING TEST ===\n")

mem = MemoryBank(path)

print("\n--- Saving a test entry ---")
mem.save_entry("This is a logging test entry.", tags=["test", "logging"])

print("\n--- Loading all entries ---")
notes = mem.load_all()
print(f"Loaded {len(notes)} entries.\n")

print("\n--- Searching entries for 'logging' ---")
results = mem.search("logging")
print(f"Search returned {len(results)} entries.\n")

print("\n--- Converting memory to text ---")
text = mem.to_text()
print(text)

print("\n=== END OF TEST ===\n")