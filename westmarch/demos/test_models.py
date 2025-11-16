# westmarch/demos/test_models.py
from westmarch.core.models import ModelClient


def test_gemini():
    client = ModelClient("Jeeves")
    response = client.call(
        system_prompt="You are Jeeves, a calm, concise English butler.",
        user_content="Please greet the user in one short, polite sentence.",
    )
    print("Gemini (Jeeves) response:\n", response)


def test_openai():
    client = ModelClient("Lady_Hawthorne")
    response = client.call(
        system_prompt="You are Lady Hawthorne, a witty aristocratic critic.",
        user_content="Offer one short, playful remark about tea.",
    )
    print("OpenAI (Lady Hawthorne) response:\n", response)


if __name__ == "__main__":
    print("=== Testing Gemini (Jeeves) ===")
    test_gemini()
    print("\n=== Testing OpenAI (Lady Hawthorne) ===")
    test_openai()