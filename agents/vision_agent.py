"""
vision_agent.py — Vision Agent for image analysis and OCR interpretation.
"""
from __future__ import annotations
import base64
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from config.logger import get_logger

logger = get_logger(__name__)

# Modelos de OpenRouter que soportan visión multimodal
_VISION_MODELS = {
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "openai/gpt-4-vision-preview",
    "anthropic/claude-3-haiku",
    "anthropic/claude-3-sonnet",
    "anthropic/claude-3-opus",
    "anthropic/claude-3-5-sonnet",
    "google/gemini-pro-vision",
    "google/gemini-flash-1.5",
    "meta-llama/llama-3.2-11b-vision-instruct",
    "meta-llama/llama-3.2-90b-vision-instruct",
}


def _model_supports_vision(llm) -> bool:
    """Detecta si el LLM actual soporta imágenes."""
    try:
        model_name = getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""
        return any(vm in model_name.lower() for vm in _VISION_MODELS)
    except Exception:
        return False


class VisionAgent:
    name = "VisionAgent"
    description = "Interprets images and OCR text."

    def __init__(self, llm: BaseChatModel) -> None:
        self._llm = llm
        self._parser = StrOutputParser()
        logger.info("VisionAgent initialised")

    def run(
        self,
        query: str,
        ocr_text: str = "",
        image_bytes: bytes | None = None,
        chat_history: list | None = None,
    ) -> str:
        """
        Analiza una imagen y responde la pregunta del usuario.
        
        Estrategia:
        1. Si hay imagen Y el modelo soporta visión → enviar imagen directamente al LLM
        2. Si hay imagen pero el modelo NO soporta visión → usar descripción técnica + OCR
        3. Si no hay imagen pero hay OCR → responder con el texto OCR
        4. Fallback: indicar que no hay imagen
        """

        # ── Caso 1: imagen + modelo con soporte visual ─────────────────────
        if image_bytes and _model_supports_vision(self._llm):
            try:
                b64 = base64.b64encode(image_bytes).decode("utf-8")
                # Detectar formato de imagen
                fmt = "jpeg"
                if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
                    fmt = "png"
                elif image_bytes[:4] == b'GIF8':
                    fmt = "gif"
                elif image_bytes[:4] == b'RIFF':
                    fmt = "webp"

                messages = [
                    SystemMessage(content=(
                        "Eres un asistente experto en análisis de imágenes. "
                        "Analiza la imagen proporcionada y responde la pregunta del usuario "
                        "de forma detallada y precisa en español."
                    )),
                    HumanMessage(content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{fmt};base64,{b64}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": query},
                    ])
                ]
                response = self._llm.invoke(messages)
                result = self._parser.invoke(response)
                logger.info("VisionAgent: multimodal response generated")
                return result
            except Exception as exc:
                logger.warning("Multimodal invoke failed: %s — falling back", exc)

        # ── Caso 2: imagen pero modelo sin visión → describir con Pillow ───
        if image_bytes:
            description = self._describe_with_pillow(image_bytes)
            combined = (
                f"Descripción técnica de la imagen: {description}\n"
            )
            if ocr_text and not ocr_text.startswith("["):
                combined += f"Texto extraído por OCR: {ocr_text}\n"
            combined += (
                f"\nPregunta del usuario: {query}\n\n"
                f"NOTA: El modelo actual no soporta análisis visual directo. "
                f"Responde basándote en la descripción técnica y el OCR disponibles."
            )
            response = self._llm.invoke(combined)
            return self._parser.invoke(response)

        # ── Caso 3: solo OCR, sin imagen ────────────────────────────────────
        if ocr_text and not ocr_text.startswith("["):
            combined = f"Texto extraído de la imagen:\n{ocr_text}\n\nPregunta: {query}"
            response = self._llm.invoke(combined)
            return self._parser.invoke(response)

        # ── Caso 4: sin imagen ni OCR ───────────────────────────────────────
        return (
            "No se ha proporcionado ninguna imagen. "
            "Por favor sube una imagen en la sección 'Upload Images' de la barra lateral "
            "antes de hacer una pregunta al Vision Agent.\n\n"
            "💡 **Tip:** Para análisis visual completo, usa un modelo con soporte de visión "
            "como `openai/gpt-4o-mini` o `meta-llama/llama-3.2-11b-vision-instruct`."
        )

    @staticmethod
    def _describe_with_pillow(image_bytes: bytes) -> str:
        """Genera descripción técnica básica con Pillow cuando no hay visión LLM."""
        try:
            import io
            import numpy as np
            from PIL import Image

            img = Image.open(io.BytesIO(image_bytes))
            w, h = img.size
            fmt = img.format or "desconocido"
            mode = img.mode

            arr = np.array(img.convert("RGB"))
            brightness = arr.mean()
            tone = "brillante" if brightness > 180 else "oscura" if brightness < 80 else "normal"

            # Detectar si tiene texto (muchos bordes = probable texto)
            gray = img.convert("L")
            gray_arr = np.array(gray, dtype=float)
            edges = abs(gray_arr[1:, :] - gray_arr[:-1, :]).mean()
            has_text_hint = "posiblemente contiene texto o diagramas" if edges > 15 else "imagen fotográfica"

            return (
                f"{w}×{h}px, formato {fmt}, modo {mode}, "
                f"iluminación {tone} (brillo={brightness:.1f}/255), {has_text_hint}."
            )
        except Exception as exc:
            return f"imagen (error al analizar: {exc})"