"""
search_tool.py — Semantic search tool over the RAG knowledge base.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.rag.retriever import DocumentRetriever

logger = get_logger(__name__)


class SearchTool:
    """Exposes RAG retrieval as a named tool."""

    name = "search_tool"
    description = "Searches the knowledge base for relevant document chunks."

    def __init__(self) -> None:
        self._retriever = DocumentRetriever()

    def search(self, query: str, k: int = 4) -> list[dict]:
        """
        Semantic search over ingested documents.

        Args:
            query: Search query string.
            k: Number of results.

        Returns:
            List of dicts: {content, source, page}.
        """
        docs = self._retriever.retrieve(query, k=k)
        return [
            {
                "content": d.page_content,
                "source": d.metadata.get("source", ""),
                "page": d.metadata.get("page", ""),
            }
            for d in docs
        ]
