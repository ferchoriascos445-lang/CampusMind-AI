"""
chains.py — LangChain LCEL chain builders.
"""
from __future__ import annotations

from datetime import date

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from campusmind.config.logger import get_logger
from campusmind.llm.prompts import (
    GENERAL_PROMPT,
    RAG_PROMPT,
    SUMMARISE_PROMPT,
)

logger = get_logger(__name__)


def _inject_date(inputs: dict) -> dict:
    """Add today's date to the inputs dict."""
    inputs.setdefault("date", date.today().isoformat())
    return inputs


def build_chat_chain(llm: BaseChatModel):
    """
    Build a simple conversational chain (no RAG).

    Returns:
        LCEL Runnable: input {input, chat_history} → str
    """
    logger.debug("Building chat chain")
    return (
        RunnableLambda(_inject_date)
        | GENERAL_PROMPT
        | llm
        | StrOutputParser()
    )


def build_rag_chain(llm: BaseChatModel):
    """
    Build a RAG-augmented conversational chain.

    Returns:
        LCEL Runnable: input {input, chat_history, context} → str
    """
    logger.debug("Building RAG chain")
    return (
        RunnableLambda(_inject_date)
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )


def build_summarise_chain(llm: BaseChatModel):
    """
    Build a document summarisation chain.

    Returns:
        LCEL Runnable: input {document_text} → str
    """
    logger.debug("Building summarise chain")
    return SUMMARISE_PROMPT | llm | StrOutputParser()
