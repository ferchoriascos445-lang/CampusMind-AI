"""
ocr_tool.py — LangChain-compatible tool wrapper for OCR.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.vision.ocr_engine import OCREngine

logger = get_logger(__name__)


class OCRTool:
    """Adapter exposing OCREngine as a simple callable tool."""

    name = "ocr_tool"
    description = "Extracts text from image files using OCR."

    def __init__(self) -> None:
        self._engine = OCREngine()

    def run(self, image_bytes: bytes, lang: str = "eng") -> str:
        """
        Extract text from image bytes.

        Args:
            image_bytes: Raw image data.
            lang: Tesseract language code.

        Returns:
            Extracted text or error message.
        """
        logger.debug("OCRTool.run called (lang=%s)", lang)
        return self._engine.extract_text(image_bytes, lang=lang)
