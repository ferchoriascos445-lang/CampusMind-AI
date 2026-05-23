"""
memory_manager.py — Unified facade for in-session and persistent memory.
"""
from __future__ import annotations

import uuid

from config.logger import get_logger
from memory.chat_memory import ChatMemory
from memory.persistent_memory import PersistentMemory

logger = get_logger(__name__)


class MemoryManager:
    """
    Facade combining ChatMemory (in-session) and PersistentMemory (SQLite).
    One instance lives in the Streamlit session_state.
    """

    def __init__(self, session_id: str | None = None) -> None:
        self._session_id = session_id or str(uuid.uuid4())
        self._chat = ChatMemory()
        self._persistent = PersistentMemory(self._session_id)
        logger.info("MemoryManager created: session=%s", self._session_id)

    @property
    def session_id(self) -> str:
        return self._session_id

    def add_user(self, message: str) -> None:
        self._chat.add_user(message)
        self._persistent.save_message("user", message)

    def add_ai(self, message: str) -> None:
        self._chat.add_ai(message)
        self._persistent.save_message("assistant", message)

    def get_chat_messages(self) -> list:
        """LangChain message objects for the chain."""
        return self._chat.get_messages()

    def get_display_messages(self) -> list[dict]:
        """Dict messages for Streamlit UI rendering."""
        return self._chat.get_as_dicts()

    def load_session(self) -> list[dict]:
        """Load persisted messages for this session from SQLite."""
        return self._persistent.load_history()

    def list_sessions(self) -> list[str]:
        return self._persistent.list_sessions()

    def clear(self) -> None:
        self._chat.clear()
        logger.info("In-session memory cleared for session=%s", self._session_id)
