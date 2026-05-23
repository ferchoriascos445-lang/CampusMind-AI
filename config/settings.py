"""
settings.py — Centralized configuration loaded from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Singleton configuration class for CampusMind AI."""

    # ── Groq (legacy, kept for backward compat) ───────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # ── OpenRouter ────────────────────────────────────────────────────────────
    OPENROUTER_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # ── LLM defaults ──────────────────────────────────────────────────────────
    DEFAULT_MODEL: str = os.getenv(
    "DEFAULT_MODEL", "meta-llama/llama-3.1-8b-instruct:free"
    )
    AVAILABLE_MODELS: list = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "meta-llama/llama-3.1-70b-instruct",
    "openai/gpt-4o-mini",
    ]
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))

    # ── Embeddings ────────────────────────────────────────────────────────────
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ── Vector stores ─────────────────────────────────────────────────────────
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./campusmind_data/chroma")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "./campusmind_data/faiss")

    # ── Database ──────────────────────────────────────────────────────────────
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./campusmind_data/history.db")

    # ── RAG ───────────────────────────────────────────────────────────────────
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "4"))

    # ── Paths ─────────────────────────────────────────────────────────────────
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "./campusmind/uploads")
    OUTPUTS_DIR: str = os.getenv("OUTPUTS_DIR", "./campusmind/outputs")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "./campusmind/logs")

    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = "CampusMind AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    def validate(self) -> None:
        """Raise if required secrets are missing."""
        if not self.OPENROUTER_API_KEY and not self.GROQ_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not set. Please add it to your environment secrets."
            )


settings = Settings()