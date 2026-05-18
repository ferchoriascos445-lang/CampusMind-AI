"""
persistent_memory.py — Persists conversation history to SQLite.
"""
from __future__ import annotations

import json
from datetime import datetime

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings
from campusmind.database.sqlite_manager import SQLiteManager

logger = get_logger(__name__)


class PersistentMemory:
    """
    Observer-style class that writes messages to SQLite for cross-session recall.
    """

    def __init__(self, session_id: str) -> None:
        self._session_id = session_id
        self._db = SQLiteManager(settings.SQLITE_DB_PATH)
        logger.debug("PersistentMemory session=%s", session_id)

    def save_message(self, role: str, content: str) -> None:
        """
        Persist a single message.

        Args:
            role: 'user' or 'assistant'.
            content: Message text.
        """
        self._db.insert_message(
            session_id=self._session_id,
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat(),
        )

    def load_history(self) -> list[dict]:
        """
        Load all messages for this session.

        Returns:
            List of {'role': ..., 'content': ..., 'timestamp': ...} dicts.
        """
        return self._db.get_messages(self._session_id)

    def list_sessions(self) -> list[str]:
        """Return all session IDs in the database."""
        return self._db.list_sessions()
