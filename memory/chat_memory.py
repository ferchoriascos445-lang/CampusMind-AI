"""
chat_memory.py — In-session conversation memory using LangChain.
"""
from __future__ import annotations

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from campusmind.config.logger import get_logger

logger = get_logger(__name__)


class ChatMemory:
    """
    Wraps ChatMessageHistory to provide typed add/get operations.
    One instance per Streamlit session.
    """

    def __init__(self) -> None:
        self._history = ChatMessageHistory()
        logger.debug("ChatMemory initialised")

    def add_user(self, message: str) -> None:
        """Add a human message."""
        self._history.add_user_message(message)

    def add_ai(self, message: str) -> None:
        """Add an AI message."""
        self._history.add_ai_message(message)

    def get_messages(self) -> list:
        """Return all messages as LangChain message objects."""
        return self._history.messages

    def get_as_dicts(self) -> list[dict]:
        """Return messages as {'role': ..., 'content': ...} dicts for UI display."""
        result = []
        for m in self._history.messages:
            if isinstance(m, HumanMessage):
                result.append({"role": "user", "content": m.content})
            elif isinstance(m, AIMessage):
                result.append({"role": "assistant", "content": m.content})
        return result

    def clear(self) -> None:
        """Reset memory."""
        self._history.clear()
        logger.debug("ChatMemory cleared")

    def __len__(self) -> int:
        return len(self._history.messages)
