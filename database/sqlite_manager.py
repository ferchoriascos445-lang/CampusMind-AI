"""
sqlite_manager.py — SQLite persistence layer for chat history.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List

from config.logger import get_logger

logger = get_logger(__name__)


class SQLiteManager:
    """
    Thread-safe SQLite manager for chat history persistence.
    Uses the connection-per-call pattern to avoid thread issues with Streamlit.
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        logger.info("SQLiteManager ready: %s", db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        """Create tables if they don't exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT    NOT NULL,
                    role       TEXT    NOT NULL,
                    content    TEXT    NOT NULL,
                    timestamp  TEXT    NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)"
            )
            conn.commit()

    def insert_message(
        self,
        session_id: str,
        role: str,
        content: str,
        timestamp: str,
    ) -> None:
        """Insert a single message row."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?,?,?,?)",
                (session_id, role, content, timestamp),
            )
            conn.commit()

    def get_messages(self, session_id: str) -> List[dict]:
        """
        Retrieve all messages for a session ordered chronologically.

        Returns:
            List of dicts with keys: role, content, timestamp.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content, timestamp FROM messages WHERE session_id=? ORDER BY id ASC",
                (session_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def list_sessions(self) -> List[str]:
        """Return distinct session IDs, most recent first."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT session_id FROM messages ORDER BY id DESC"
            ).fetchall()
        return [r["session_id"] for r in rows]

    def delete_session(self, session_id: str) -> None:
        """Remove all messages for a session."""
        with self._connect() as conn:
            conn.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
            conn.commit()
        logger.info("Deleted session: %s", session_id)
