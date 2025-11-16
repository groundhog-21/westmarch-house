from westmarch.agents.miss_pennington import MissPenningtonAgent
from westmarch.core.models import ModelClient

pen = MissPenningtonAgent(ModelClient("Miss Pennington"))

print("Calling Pennington...")

result = pen.model_client.call(
    system_prompt="You are Miss Pennington.",
    user_content="Rewrite this into a polite email: I need the report tomorrow."
)

print("RESULT:", result)