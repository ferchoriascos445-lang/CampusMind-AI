"""
research_agent.py — Research Agent for academic research methodology.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from campusmind.config.logger import get_logger
from campusmind.llm.prompts import RESEARCH_PROMPT

logger = get_logger(__name__)


class ResearchAgent:
    """
    Specialised agent for research tasks: methodology, literature review,
    data analysis interpretation, and scientific writing.
    """

    name = "ResearchAgent"
    description = "Expert in research methodology, literature review, and data analysis."

    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = RESEARCH_PROMPT | llm | StrOutputParser()
        logger.info("ResearchAgent initialised")

    def run(self, query: str, chat_history: list | None = None) -> str:
        """
        Process a research-related query.

        Args:
            query: Research question or methodology task.
            chat_history: Previous messages for context.

        Returns:
            Agent response string.
        """
        logger.debug("ResearchAgent query: %s…", query[:60])
        return self._chain.invoke({
            "input": query,
            "chat_history": chat_history or [],
        })
