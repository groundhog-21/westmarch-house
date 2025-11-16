# westmarch/core/models.py
from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

from westmarch.core.logging import log

# Load .env variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Gemini (AI Studio)
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Configure OpenAI
openai_client: Optional[OpenAI] = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


class ModelClient:
    """
    Unified model client for all Westmarch agents.

    - Jeeves, Perkins, Miss Pennington -> Gemini (gemini-1.5-flash)
    - Lady Hawthorne                   -> OpenAI GPT (gpt-4.1)
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name.lower()

        if self.agent_name in {"lady_hawthorne", "lady hawthorne"}:
            self.provider = "openai"
            self.model_name = "gpt-4.1"          # adjust if you prefer gpt-4o / gpt-4o-mini
        else:
            self.provider = "gemini"
            self.model_name = "gemini-2.5-flash-lite"  # current fast, cost-effective model

    def call(self, system_prompt: str, user_content: str) -> str:
        """
        Main entry point used by all agents.
        Combines the agent's system prompt and the constructed user content,
        and routes the call to Gemini or OpenAI.
        """
        system_prompt = (system_prompt or "").strip()
        user_content = (user_content or "").strip()

        if self.provider == "gemini":
            if not GOOGLE_API_KEY:
                return "[Gemini Error: GOOGLE_API_KEY not set in .env]"

            try:
                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: calling GEMINI model '{self.model_name}'")
                log(f"System prompt: {system_prompt[:80]}...")
                log(f"User content: {user_content[:80]}...")

                model = genai.GenerativeModel(self.model_name)
                # For Gemini we just send one combined prompt
                full_prompt = f"{system_prompt}\n\n{user_content}".strip()
                response = model.generate_content(full_prompt)

                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: model call completed")

                return getattr(response, "text", str(response))
            
            except Exception as e:
                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: ERROR during Gemini call → {e}")
                return f"[Gemini Error: {e}]"

        if self.provider == "openai":
            if not OPENAI_API_KEY or openai_client is None:
                return "[OpenAI Error: OPENAI_API_KEY not set in .env]"

            try:
                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: calling OPENAI model '{self.model_name}'")
                log(f"System prompt: {system_prompt[:80]}...")
                log(f"User content: {user_content[:80]}...")

                response = openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    max_tokens=800,
                )

                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: model call completed")
                
                return response.choices[0].message.content
            
            except Exception as e:
                # >>> LOGGING INSERTED HERE <<<
                log(f"{self.agent_name}: ERROR during OpenAI call → {e}")
                return f"[OpenAI Error: {e}]"

        return "[Error: Unknown provider]"