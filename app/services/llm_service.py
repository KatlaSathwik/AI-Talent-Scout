"""
LLM abstraction service for Gemini-based interactions.
"""
from __future__ import annotations

import json
from typing import Any, Dict

import google.genai as genai
from google.genai.types import GenerateContentConfig

from app.config import settings


class LLMService:
    """Provider-agnostic LLM interface (currently Gemini)."""

    def __init__(self) -> None:
        """Initialize Gemini client and model."""
        if settings.LLM_PROVIDER.lower() != "gemini":
            raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.MODEL_NAME

    def generate_text(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate deterministic text output from Gemini."""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=temperature,
                top_p=0.95,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise ValueError("Empty response from Gemini")
        return text.strip()

    def generate_json(self, prompt: str, temperature: float = 0.1) -> Dict[str, Any]:
        """Generate JSON output from Gemini with basic robust parsing."""
        raw = self.generate_text(prompt, temperature=temperature)

        # Try strict JSON first
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON block
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            snippet = raw[start : end + 1]
            return json.loads(snippet)

        raise ValueError("Gemini output is not valid JSON")
