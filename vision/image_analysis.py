"""
image_analysis.py — Image description and analysis utilities.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.vision.ocr_engine import OCREngine

logger = get_logger(__name__)


class ImageAnalyzer:
    """
    Provides image analysis features:
    - Basic metadata extraction
    - OCR text extraction
    - Colour statistics
    - Simple classification heuristics
    """

    def __init__(self) -> None:
        self._ocr = OCREngine()

    def analyze(self, image_bytes: bytes, run_ocr: bool = True) -> dict:
        """
        Full image analysis pipeline.

        Args:
            image_bytes: Raw image data.
            run_ocr: Whether to run OCR on the image.

        Returns:
            Analysis dict with keys: info, ocr_text, color_stats, description.
        """
        result: dict = {}

        # Basic image info
        result["info"] = OCREngine.get_image_info(image_bytes)

        # OCR
        if run_ocr:
            result["ocr_text"] = self._ocr.extract_text(image_bytes)
        else:
            result["ocr_text"] = ""

        # Colour stats
        result["color_stats"] = self._color_stats(image_bytes)

        # Simple text description
        result["description"] = self._describe(result)

        return result

    @staticmethod
    def _color_stats(image_bytes: bytes) -> dict:
        """Compute basic colour statistics."""
        try:
            import io
            import numpy as np
            from PIL import Image

            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            arr = np.array(img)
            return {
                "mean_r": float(arr[:, :, 0].mean()),
                "mean_g": float(arr[:, :, 1].mean()),
                "mean_b": float(arr[:, :, 2].mean()),
                "brightness": float(arr.mean()),
            }
        except Exception:
            return {}

    @staticmethod
    def _describe(analysis: dict) -> str:
        """Build a plain-English summary of the analysis."""
        info = analysis.get("info", {})
        w, h = info.get("width", "?"), info.get("height", "?")
        fmt = info.get("format", "unknown")
        ocr = analysis.get("ocr_text", "")
        stats = analysis.get("color_stats", {})
        brightness = stats.get("brightness", None)

        desc = f"Image: {w}×{h}px, format={fmt}."
        if brightness is not None:
            tone = "bright" if brightness > 128 else "dark"
            desc += f" Overall tone: {tone} (brightness={brightness:.1f}/255)."
        if ocr and not ocr.startswith("["):
            snippet = ocr[:200].replace("\n", " ")
            desc += f" OCR text found ({len(ocr)} chars): \"{snippet}…\""
        return desc
