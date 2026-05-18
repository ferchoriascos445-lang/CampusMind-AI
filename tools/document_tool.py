"""
document_tool.py — Tool for loading and summarising documents.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.rag.document_loader import DocumentLoader

logger = get_logger(__name__)


class DocumentTool:
    """Loads and returns document text for downstream use."""

    name = "document_tool"
    description = "Loads documents (PDF, DOCX, TXT, CSV) and returns their text content."

    def __init__(self) -> None:
        self._loader = DocumentLoader()

    def load_text(self, file_bytes: bytes, filename: str) -> str:
        """
        Load a document and return concatenated text.

        Args:
            file_bytes: Raw file bytes.
            filename: Original filename.

        Returns:
            Concatenated text content.
        """
        docs = self._loader.load_from_bytes(file_bytes, filename)
        text = "\n\n".join(d.page_content for d in docs)
        logger.info("DocumentTool loaded '%s' (%d chars)", filename, len(text))
        return text
