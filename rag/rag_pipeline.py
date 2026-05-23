"""
rag_pipeline.py — End-to-end RAG pipeline: ingest + query.
"""
from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from config.logger import get_logger
from embeddings.embedding_manager import EmbeddingManager
from rag.document_loader import DocumentLoader
from rag.retriever import DocumentRetriever
from rag.splitter import DocumentSplitter
from vectorstore.vector_factory import VectorStoreFactory

logger = get_logger(__name__)
_em = EmbeddingManager()


class RAGPipeline:
    """
    Orchestrates the full Retrieval-Augmented Generation pipeline.

    Ingest path:  file_bytes → load → split → embed → store
    Query path:   question → retrieve → format_context → LLM
    """

    def __init__(self, backend: str = "chroma", collection: str = "campusmind") -> None:
        self._loader = DocumentLoader()
        self._splitter = DocumentSplitter()
        self._retriever = DocumentRetriever(backend=backend, collection=collection)
        self._manager = VectorStoreFactory.get_manager(backend, collection)
        self._ingested_files: List[str] = []

    def ingest(self, file_bytes: bytes, filename: str) -> int:
        """
        Load, split, and embed a file into the vector store.

        Args:
            file_bytes: Raw file content.
            filename: Original file name (determines parser).

        Returns:
            Number of chunks ingested.
        """
        docs = self._loader.load_from_bytes(file_bytes, filename)
        chunks = self._splitter.split(docs)
        embeddings = _em.get_embeddings()
        self._manager.add_documents(chunks, embeddings)
        self._ingested_files.append(filename)
        logger.info("Ingested '%s' → %d chunks", filename, len(chunks))
        return len(chunks)

    def get_context(self, query: str, k: int | None = None) -> str:
        """
        Retrieve relevant context for a query.

        Args:
            query: User question.
            k: Number of chunks to retrieve.

        Returns:
            Formatted context string for the LLM prompt.
        """
        docs = self._retriever.retrieve(query, k=k)
        return self._retriever.format_context(docs)

    @property
    def ingested_files(self) -> List[str]:
        return list(self._ingested_files)

    def reset(self) -> None:
        """Clear all ingested documents from the vector store."""
        embeddings = _em.get_embeddings()
        self._manager.reset(embeddings)
        self._ingested_files.clear()
        logger.warning("RAG pipeline reset — all documents removed")
