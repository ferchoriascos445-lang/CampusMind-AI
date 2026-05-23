"""
image_tool.py — Tool for image analysis and captioning.
"""
from __future__ import annotations

from config.logger import get_logger
from vision.image_analysis import ImageAnalyzer
from vision.image_captioning import ImageCaptioner

logger = get_logger(__name__)


class ImageTool:
    """Combines ImageAnalyzer and ImageCaptioner into one callable tool."""

    name = "image_tool"
    description = "Analyzes images: OCR, colour stats, and natural-language description."

    def __init__(self) -> None:
        self._analyzer = ImageAnalyzer()
        self._captioner = ImageCaptioner()

    def analyze(self, image_bytes: bytes) -> dict:
        """Full analysis: metadata + OCR + colour stats."""
        return self._analyzer.analyze(image_bytes)

    def caption(self, image_bytes: bytes, llm=None) -> str:
        """Generate a natural-language caption (optionally LLM-enriched)."""
        return self._captioner.caption(image_bytes, llm=llm)
