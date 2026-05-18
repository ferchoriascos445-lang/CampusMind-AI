"""
retriever.py — Semantic retriever that queries the vector store.
"""
from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings
from campusmind.embeddings.embedding_manager import EmbeddingManager
from campusmind.vectorstore.vector_factory import VectorStoreFactory

logger = get_logger(__name__)
_em = EmbeddingManager()


class DocumentRetriever:
    """
    Semantic retrieval over the active vector store.
    """

    def __init__(self, backend: str = "chroma", collection: str = "campusmind") -> None:
        self._manager = VectorStoreFactory.get_manager(backend, collection)

    def retrieve(self, query: str, k: int | None = None) -> List[Document]:
        """
        Retrieve the top-k most relevant document chunks for a query.

        Args:
            query: User question or search string.
            k: Number of results (defaults to settings.RETRIEVAL_K).

        Returns:
            List of relevant Document chunks.
        """
        embeddings = _em.get_embeddings()
        retriever = self._manager.as_retriever(embeddings, k=k or settings.RETRIEVAL_K)
        docs = retriever.invoke(query)
        logger.debug("Retrieved %d docs for query: %s…", len(docs), query[:60])
        return docs

    def format_context(self, docs: List[Document]) -> str:
        """
        Format retrieved documents into a single context string.

        Args:
            docs: Retrieved document chunks.

        Returns:
            Concatenated context string with source metadata.
        """
        parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "")
            header = f"[Document {i} | {source}" + (f" | p.{page}" if page else "") + "]"
            parts.append(f"{header}\n{doc.page_content}")
        return "\n\n---\n\n".join(parts)
