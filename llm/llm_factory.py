"""
llm_factory.py — Factory pattern for creating LLM instances.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings
from campusmind.llm.openrouter_client import OpenRouterClient

logger = get_logger(__name__)

_openrouter_client = OpenRouterClient()


class LLMFactory:
    """Factory for producing configured LLM instances (Strategy pattern)."""

    @staticmethod
    def create(
        provider: str = "openrouter",
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> BaseChatModel:
        if provider in ("openrouter", "groq"):
            return _openrouter_client.get_llm(
                model=model or settings.DEFAULT_MODEL,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        raise ValueError(f"Unsupported LLM provider: '{provider}'")