"""
query_engine.py — High-level query interface combining retrieval + LLM.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel

from config.logger import get_logger
from llm.chains import build_rag_chain
from rag.retriever import DocumentRetriever

logger = get_logger(__name__)


class QueryEngine:
    """
    End-to-end RAG query engine: retrieve → format context → generate answer.
    """

    def __init__(self, llm: BaseChatModel, backend: str = "chroma") -> None:
        self._retriever = DocumentRetriever(backend=backend)
        self._chain = build_rag_chain(llm)
        logger.info("QueryEngine initialised")

    def query(
        self,
        question: str,
        chat_history: list | None = None,
        k: int | None = None,
    ) -> dict:
        """
        Run a RAG query.

        Args:
            question: User question.
            chat_history: Previous message objects.
            k: Number of chunks to retrieve.

        Returns:
            Dict with 'answer' (str) and 'sources' (list of str).
        """
        docs = self._retriever.retrieve(question, k=k)
        context = self._retriever.format_context(docs)
        sources = list({d.metadata.get("source", "unknown") for d in docs})

        answer = self._chain.invoke({
            "input": question,
            "chat_history": chat_history or [],
            "context": context,
        })

        logger.info("QueryEngine answered using %d docs from %s", len(docs), sources)
        return {"answer": answer, "sources": sources}
