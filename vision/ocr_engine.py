"""
ocr_engine.py — OCR extraction using pytesseract (with graceful fallback).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from campusmind.config.logger import get_logger

logger = get_logger(__name__)


class OCREngine:
    """
    Extracts text from images using pytesseract.
    Falls back gracefully if Tesseract binary is not installed.
    """

    @staticmethod
    def extract_text(image_bytes: bytes, lang: str = "eng") -> str:
        """
        Run OCR on raw image bytes.

        Args:
            image_bytes: Raw image data (PNG, JPG, etc.).
            lang: Tesseract language code (e.g. 'eng', 'spa', 'eng+spa').

        Returns:
            Extracted text string, or an error message if OCR unavailable.
        """
        try:
            import io
            import pytesseract
            from PIL import Image

            img = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(img, lang=lang)
            logger.info("OCR complete: %d chars extracted", len(text))
            return text.strip()
        except ImportError:
            msg = (
                "[OCR unavailable] pytesseract is not installed or "
                "Tesseract binary is missing. Install tesseract-ocr and pytesseract."
            )
            logger.warning(msg)
            return msg
        except Exception as exc:
            logger.error("OCR error: %s", exc)
            return f"[OCR error] {exc}"

    @staticmethod
    def get_image_info(image_bytes: bytes) -> dict:
        """
        Return basic image metadata.

        Args:
            image_bytes: Raw image data.

        Returns:
            Dict with width, height, mode, format.
        """
        try:
            import io
            from PIL import Image

            img = Image.open(io.BytesIO(image_bytes))
            return {
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format or "unknown",
            }
        except Exception as exc:
            logger.error("Image info error: %s", exc)
            return {}
