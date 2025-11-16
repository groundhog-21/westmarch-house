from dotenv import load_dotenv
import os

load_dotenv()

print("GOOGLE_API_KEY:", bool(os.getenv("GOOGLE_API_KEY")))
print("OPENAI_API_KEY:", bool(os.getenv("OPENAI_API_KEY")))