"""
splitter.py — Text splitting strategies for chunking documents.
"""
from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


class DocumentSplitter:
    """
    Splits raw Documents into overlapping chunks suitable for embedding.
    Uses RecursiveCharacterTextSplitter (respects paragraph/sentence boundaries).
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        logger.debug(
            "Splitter initialised: chunk_size=%d overlap=%d",
            self.chunk_size,
            self.chunk_overlap,
        )

    def split(self, documents: List[Document]) -> List[Document]:
        """
        Split a list of Documents into smaller chunks.

        Args:
            documents: Raw document list from DocumentLoader.

        Returns:
            List of smaller Document chunks with preserved metadata.
        """
        chunks = self._splitter.split_documents(documents)
        logger.info("Split %d docs → %d chunks", len(documents), len(chunks))
        return chunks
