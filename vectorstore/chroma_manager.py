"""
chroma_manager.py — ChromaDB vector store manager.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings

logger = get_logger(__name__)


class ChromaManager:
    """
    Manages a ChromaDB vector store (persist on disk).
    Implements Singleton per collection name.
    """

    _instances: dict[str, "ChromaManager"] = {}

    def __new__(cls, collection_name: str = "campusmind") -> "ChromaManager":
        if collection_name not in cls._instances:
            instance = super().__new__(cls)
            instance._collection_name = collection_name
            instance._initialized = False
            cls._instances[collection_name] = instance
        return cls._instances[collection_name]

    def __init__(self, collection_name: str = "campusmind") -> None:
        if self._initialized:
            return
        self._initialized = True
        self._store: Chroma | None = None
        persist_dir = Path(settings.CHROMA_PERSIST_DIR)
        persist_dir.mkdir(parents=True, exist_ok=True)
        self._persist_dir = str(persist_dir)
        logger.info("ChromaManager ready: collection=%s", collection_name)

    def get_or_create(self, embeddings: Embeddings) -> Chroma:
        """
        Return existing store or create a new one.

        Args:
            embeddings: Embedding function to use.

        Returns:
            Chroma vector store instance.
        """
        if self._store is None:
            self._store = Chroma(
                collection_name=self._collection_name,
                embedding_function=embeddings,
                persist_directory=self._persist_dir,
            )
            logger.info("ChromaDB store created/loaded from %s", self._persist_dir)
        return self._store

    def add_documents(self, docs: List[Document], embeddings: Embeddings) -> None:
        """
        Embed and add documents to the store.

        Args:
            docs: Document chunks to add.
            embeddings: Embedding function.
        """
        store = self.get_or_create(embeddings)
        store.add_documents(docs)
        logger.info("Added %d documents to ChromaDB", len(docs))

    def as_retriever(self, embeddings: Embeddings, k: int | None = None):
        """
        Return a retriever interface over the store.

        Args:
            embeddings: Embedding function.
            k: Number of results to retrieve.

        Returns:
            VectorStoreRetriever.
        """
        store = self.get_or_create(embeddings)
        return store.as_retriever(
            search_kwargs={"k": k or settings.RETRIEVAL_K}
        )

    def reset(self, embeddings: Embeddings) -> None:
        """Clear all documents from the collection."""
        store = self.get_or_create(embeddings)
        store.delete_collection()
        self._store = None
        logger.warning("ChromaDB collection '%s' cleared", self._collection_name)
