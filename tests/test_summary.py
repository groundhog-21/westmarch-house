from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.core.models import ModelClient


def run():
    pennington = MissPenningtonAgent(ModelClient("Miss Pennington"))

    print("=== Saving notes ===")
    pennington.save_note("The user enjoys Victorian-era crime fiction.")
    pennington.save_note("The user prefers early-morning planning sessions.")
    pennington.save_note("The user travels frequently to the U.S. East Coast.")

    print("\n=== Summary ===")
    summary = pennington.summarize_memory()
    print(summary)


if __name__ == "__main__":
    run()