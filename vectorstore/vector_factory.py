"""
vector_factory.py — Factory for creating vector store backends (Strategy pattern).
"""
from __future__ import annotations

from langchain_core.embeddings import Embeddings

from campusmind.config.constants import VECTOR_BACKEND_CHROMA
from campusmind.config.logger import get_logger
from campusmind.vectorstore.chroma_manager import ChromaManager

logger = get_logger(__name__)


class VectorStoreFactory:
    """Creates and returns the appropriate vector store backend."""

    @staticmethod
    def get_manager(backend: str = VECTOR_BACKEND_CHROMA, collection: str = "campusmind"):
        """
        Return a vector store manager for the requested backend.

        Args:
            backend: 'chroma' (default).
            collection: Collection/index name.

        Returns:
            ChromaManager instance.

        Raises:
            ValueError: For unsupported backends.
        """
        if backend == VECTOR_BACKEND_CHROMA:
            logger.debug("Vector backend: ChromaDB (collection=%s)", collection)
            return ChromaManager(collection_name=collection)
        raise ValueError(f"Unsupported vector backend: '{backend}'")
