from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.core.models import ModelClient

def run():
    pennington = MissPenningtonAgent(ModelClient("Miss Pennington"))

    print("Saving a note...")
    pennington.save_note("The user enjoys historical crime fiction.")
    pennington.save_note("Reminder: Book trip itinerary to U.S.")

    print("All notes:")
    for note in pennington.recall_all():
        print(note)

    print("Search 'crime':")
    for note in pennington.search_memory("crime"):
        print(note)

if __name__ == "__main__":
    run()