# westmarch/core/models.py
from __future__ import annotations
from typing import Any


class ModelClient:
    """
    A thin wrapper around LLM APIs (Gemini, OpenAI).
    For now it returns a mock response until we wire in the real clients.
    """

    def __init__(self, provider: str, model_name: str, api_key: str | None = None):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key

    def call(self, system_prompt: str, user_content: str) -> str:
        # Placeholder for now — to be replaced with real API calls.
        return f"[{self.provider}:{self.model_name} MOCK RESPONSE]\n{user_content}"