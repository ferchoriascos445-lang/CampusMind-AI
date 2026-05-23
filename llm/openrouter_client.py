"""
openrouter_client.py — OpenRouter API client (Singleton pattern).
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from config.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterClient:
    """Singleton wrapper around ChatOpenAI pointed at OpenRouter."""

    _instance: OpenRouterClient | None = None

    def __new__(cls) -> "OpenRouterClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        logger.info("Initialising OpenRouterClient singleton")

    def get_llm(
        self,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatOpenAI:
        model = model or settings.DEFAULT_MODEL
        temperature = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE
        max_tokens = max_tokens or settings.MAX_TOKENS

        logger.debug("Creating ChatOpenAI (OpenRouter): model=%s temp=%.2f", model, temperature)
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )