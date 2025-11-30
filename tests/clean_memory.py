import json
import os

# ---- CLEANED MEMORY CONTENT ----
CLEANED_MEMORY = [
  {
    "timestamp": "2025-01-01T00:00:00",
    "content": "A Short History of the Westmarch Estate (Selected Highlights)\n\n\u2022 1066 \u2014 The original Westmarch lands were granted to Sir Archibald Thistlewick II for \u201cservices rendered,\u201d though the exact nature of these services remains politely unrecorded.\n\n\u2022 1324 \u2014 The first manor house was erected after Sir Lionel Thistlewick accidentally burned down the previous structure while attempting to demonstrate a new \u201cportable fireplace.\u201d\n\n\u2022 1587 \u2014 Lady Constance Westmarch introduced the estate\u2019s famed tradition of maintaining a library larger than the dining hall, arguing that \u201cideas nourish more deeply than soups.\u201d\n\n\u2022 1712 \u2014 The Great Teapot Ordinance was issued following an incident in which the household went 11 minutes without tea. New servants were thereafter required to pass a Teapot Readiness Inspection.\n\n\u2022 1793 \u2014 The West Wing was rebuilt after a minor misunderstanding involving fireworks, a rogue pheasant, and Lord Westmarch\u2019s experimental weather-vane cannon.\n\n\u2022 1841 \u2014 The estate gained notoriety when noted naturalist Percival Greeley claimed to have discovered a new mammal species in the gardens. It was later determined to be the gardener in his winter coat.\n\n\u2022 1906 \u2014 Miss Euphemia Pennington (an ancestor of our current archivist) introduced the Westmarch Filing Codex, which required all household documents to be annotated, indexed, and lightly perfumed.\n\n\u2022 1938 \u2014 The arrival of the first mechanical \u201clabor-saving devices\u201d led to the Westmarch House Rebellion, in which the staff refused to trust any appliance capable of humming ominously.\n\n\u2022 1994 \u2014 The now-infamous Westmarch Garden Gnome Incident began, involving nocturnal relocations, suspicious tip-toeing noises, and several eyewitness accounts described as \u201cunhelpfully whimsical.\u201d\n\n\u2022 2025 \u2014 The modern Westmarch Estate was digitized, allowing Jeeves, Perkins, Miss Pennington, and Lady Hawthorne to maintain the household\u2019s long-standing traditions with unprecedented efficiency \u2014 though the gnome continues to wander when unobserved.",
    "tags": [
      "history",
      "westmarch",
      "archive"
    ]
  },
  {
    "timestamp": "2025-11-22T07:41:16.665923",
    "content": "Critique requested from Lady Hawthorne:\n\nTEXT:\nJeeves, my good man, I have composed a short poem. Would you be so kind as to present it to Her Ladyship for her\u2026 unvarnished appraisal?\u201d\n\nHere it is:\n\nO Languid Moon of Yesteryear\n\nO languid moon of yesteryear,\nWhy do you hang so low and tired\nAbove the wilted hopes I\u2019ve scattered\nOn the garden path of memory?\nEach petal droops with whispered truths\nI dared not speak at suppertime,\nAnd every sigh becomes a gust\nThat stirs the ashes of my dreams.\nThe teapot weeps its porcelain tears\u2014\nIt knows the weight of my regret.\nO moon, descend and hear my plea:\nReturn the Tuesdays I have lost.\n\nCRITIQUE:\nAh, what a wistful tableau you have painted\u2026",
    "tags": [
      "poetry",
      "critique"
    ]
  },
  {
    "timestamp": "2025-11-24T09:14:22.991001",
    "content": "Parlour discussion entry:\nUSER SAID: My dear staff, I require assistance with a peculiar event: the garden gnome\u2026\nJEEVES REPLIED: Ah, Master, a perplexing development indeed\u2026",
    "tags": [
      "parlour",
      "gnome"
    ]
  },
  {
    "timestamp": "2025-11-24T09:18:44.221001",
    "content": "Research performed for user request:\nREQUEST: Perkins, I require you to investigate a peculiar event\u2026\nRESEARCH SUMMARY:\nObservation: gnome moved two paving stones\u2026",
    "tags": [
      "research",
      "gnome"
    ]
  },
  {
    "timestamp": "2025-11-24T09:30:11.441001",
    "content": "Drafted text based on user request:\nREQUEST: Draft a short, extremely polite note to the neighbours\u2026\nDRAFT: Dear Neighbours\u2026",
    "tags": [
      "draft",
      "gnome",
      "letter"
    ]
  },
  {
    "timestamp": "2025-11-24T14:21:51.512311",
    "content": "Research performed for user request:\nREQUEST: Research the difference between ETFs and mutual funds.\nRESEARCH SUMMARY:\nComparison of ETFs vs mutual funds\u2026",
    "tags": [
      "finance",
      "research"
    ]
  }
]

# ---------- MAIN CLEANUP SCRIPT ----------

def clean_memory(memory_path="westmarch/data/memory.json"):
    print(f"Loading memory file from: {memory_path}")

    if not os.path.exists(memory_path):
        print("ERROR: memory.json not found.")
        return

    # Backup first
    backup_path = memory_path + ".backup"
    with open(memory_path, "r", encoding="utf-8") as f:
        original = json.load(f)
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(original, f, indent=2)
    print(f"Backup created → {backup_path}")

    # Write cleaned version
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(CLEANED_MEMORY, f, indent=2)

    print("memory.json cleaned and overwritten successfully.")
    print(f"Entries kept: {len(CLEANED_MEMORY)}")


if __name__ == "__main__":
    clean_memory()