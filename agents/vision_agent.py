"""
vision_agent.py — Vision Agent for image analysis and OCR interpretation.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from campusmind.config.logger import get_logger
from campusmind.llm.prompts import VISION_PROMPT

logger = get_logger(__name__)


class VisionAgent:
    """
    Specialised agent that interprets OCR output and image descriptions,
    helping users understand and work with visual content.
    """

    name = "VisionAgent"
    description = "Interprets OCR text and image analysis results."

    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = VISION_PROMPT | llm | StrOutputParser()
        logger.info("VisionAgent initialised")

    def run(
        self,
        query: str,
        ocr_text: str = "",
        chat_history: list | None = None,
    ) -> str:
        """
        Process a vision/OCR-related query.

        Args:
            query: User question about the image/OCR content.
            ocr_text: Extracted OCR text to include in context.
            chat_history: Previous messages.

        Returns:
            Agent response string.
        """
        combined = query
        if ocr_text:
            combined = f"OCR extracted text:\n{ocr_text}\n\nUser question: {query}"

        logger.debug("VisionAgent query: %s…", query[:60])
        return self._chain.invoke({
            "input": combined,
            "chat_history": chat_history or [],
        })
