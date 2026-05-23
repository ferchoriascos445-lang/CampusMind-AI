"""
embedding_manager.py — Manages embedding models (Singleton + Strategy pattern).
"""
from __future__ import annotations

from langchain_core.embeddings import Embeddings

from config.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class EmbeddingManager:
    """
    Singleton that provides a shared Embeddings instance.
    Uses ChromaDB's built-in fast embedding by default to avoid heavy deps.
    Falls back gracefully if HuggingFace is unavailable.
    """

    _instance: "EmbeddingManager | None" = None
    _embeddings: Embeddings | None = None

    def __new__(cls) -> "EmbeddingManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_embeddings(self) -> Embeddings:
        """
        Return a cached Embeddings instance.

        Tries HuggingFaceEmbeddings first; falls back to a lightweight
        ChromaDB-compatible default embedding.

        Returns:
            Embeddings instance.
        """
        if self._embeddings is not None:
            return self._embeddings

        # Try HuggingFace sentence-transformers (optional heavy dep)
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            logger.info("Using HuggingFaceEmbeddings: %s", settings.EMBEDDING_MODEL)
            return self._embeddings
        except Exception:
            pass

        # Fallback: use Chroma's default embedding (no external download)
        try:
            from chromadb.utils.embedding_functions import (
                DefaultEmbeddingFunction,
            )
            from langchain_core.embeddings import Embeddings as BaseEmb

            class _ChromaDefaultEmbeddings(BaseEmb):
                """Thin LangChain wrapper around ChromaDB's built-in embedder."""

                def __init__(self) -> None:
                    self._fn = DefaultEmbeddingFunction()

                def embed_documents(self, texts):
                    return self._fn(texts)

                def embed_query(self, text):
                    return self._fn([text])[0]

            self._embeddings = _ChromaDefaultEmbeddings()
            logger.info("Using ChromaDB default embeddings (fallback)")
            return self._embeddings
        except Exception as exc:
            logger.error("Could not load any embedding model: %s", exc)
            raise RuntimeError("No embedding backend available") from exc
