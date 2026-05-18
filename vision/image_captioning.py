"""
image_captioning.py — LLM-based image captioning via description prompt.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.vision.image_analysis import ImageAnalyzer

logger = get_logger(__name__)


class ImageCaptioner:
    """
    Generates natural-language captions for images by combining
    OCR output and colour analysis, then asking the LLM to describe them.
    """

    def __init__(self) -> None:
        self._analyzer = ImageAnalyzer()

    def caption(self, image_bytes: bytes, llm=None) -> str:
        """
        Generate a caption for the image.

        Args:
            image_bytes: Raw image data.
            llm: Optional LangChain LLM to enrich the caption.

        Returns:
            Caption string.
        """
        analysis = self._analyzer.analyze(image_bytes, run_ocr=True)
        base_desc = analysis.get("description", "")
        ocr_text = analysis.get("ocr_text", "")

        if llm is not None:
            try:
                prompt = (
                    f"Describe this image based on the following analysis:\n\n"
                    f"Technical description: {base_desc}\n"
                    f"OCR text found: {ocr_text[:500] if ocr_text else 'None'}\n\n"
                    "Provide a concise, informative description of what this image likely shows."
                )
                response = llm.invoke(prompt)
                caption = response.content if hasattr(response, "content") else str(response)
                logger.info("LLM caption generated (%d chars)", len(caption))
                return caption
            except Exception as exc:
                logger.warning("LLM captioning failed: %s — using base description", exc)

        return base_desc
