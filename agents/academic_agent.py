"""
academic_agent.py — Academic Agent for university-level academic tasks.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from campusmind.config.logger import get_logger
from campusmind.llm.prompts import ACADEMIC_PROMPT

logger = get_logger(__name__)


class AcademicAgent:
    """
    Specialised agent for academic tasks: essay help, citations,
    concept explanation, and subject-specific Q&A.
    """

    name = "AcademicAgent"
    description = "Expert in academic writing, citations, and subject-matter explanation."

    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = ACADEMIC_PROMPT | llm | StrOutputParser()
        logger.info("AcademicAgent initialised")

    def run(self, query: str, chat_history: list | None = None) -> str:
        """
        Process an academic query.

        Args:
            query: User's academic question or task.
            chat_history: Previous messages for context.

        Returns:
            Agent response string.
        """
        logger.debug("AcademicAgent query: %s…", query[:60])
        return self._chain.invoke({
            "input": query,
            "chat_history": chat_history or [],
        })
