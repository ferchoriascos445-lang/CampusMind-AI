"""
controllers.py — Business logic controllers used by the Streamlit app.
"""
from __future__ import annotations

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings
from campusmind.llm.chains import build_chat_chain, build_rag_chain, build_summarise_chain
from campusmind.llm.llm_factory import LLMFactory
from campusmind.memory.memory_manager import MemoryManager
from campusmind.rag.rag_pipeline import RAGPipeline

logger = get_logger(__name__)


class ChatController:
    """
    Handles all LLM interaction: plain chat, RAG-augmented chat, and summarisation.
    One instance per Streamlit session.
    """

    def __init__(
        self,
        memory: MemoryManager,
        rag: RAGPipeline,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        self._memory = memory
        self._rag = rag
        self._model = model or settings.DEFAULT_MODEL
        self._temperature = temperature if temperature is not None else settings.DEFAULT_TEMPERATURE
        self._llm = LLMFactory.create(model=self._model, temperature=self._temperature)
        self._chat_chain = build_chat_chain(self._llm)
        self._rag_chain = build_rag_chain(self._llm)
        self._summarise_chain = build_summarise_chain(self._llm)
        logger.info("ChatController initialised: model=%s temp=%.2f", self._model, self._temperature)

    def update_model(self, model: str, temperature: float) -> None:
        """Hot-swap the LLM without losing memory."""
        self._model = model
        self._temperature = temperature
        self._llm = LLMFactory.create(model=model, temperature=temperature)
        self._chat_chain = build_chat_chain(self._llm)
        self._rag_chain = build_rag_chain(self._llm)
        self._summarise_chain = build_summarise_chain(self._llm)
        logger.info("Model updated: %s @ %.2f", model, temperature)

    def chat(self, user_input: str, use_rag: bool = False) -> str:
        """
        Send a message and get an AI response.

        Args:
            user_input: The user's message.
            use_rag: Whether to retrieve context from the vector store first.

        Returns:
            AI response string.
        """
        self._memory.add_user(user_input)
        chat_history = self._memory.get_chat_messages()[:-1]  # Exclude last user msg

        try:
            if use_rag and self._rag.ingested_files:
                context = self._rag.get_context(user_input)
                response = self._rag_chain.invoke({
                    "input": user_input,
                    "chat_history": chat_history,
                    "context": context,
                })
            else:
                response = self._chat_chain.invoke({
                    "input": user_input,
                    "chat_history": chat_history,
                })
        except Exception as exc:
            logger.error("Chat error: %s", exc)
            response = f"Error generating response: {exc}"

        self._memory.add_ai(response)
        return response

    def summarise(self, document_text: str) -> str:
        """Summarise a document using the LLM."""
        try:
            return self._summarise_chain.invoke({"document_text": document_text})
        except Exception as exc:
            logger.error("Summarise error: %s", exc)
            return f"Summarisation error: {exc}"

    def run_agent(
        self,
        agent_type: str,
        user_input: str,
        ocr_text: str = "",
    ) -> str:
        """
        Run a specialised agent and persist the exchange.

        Args:
            agent_type: 'academic', 'research', or 'vision'.
            user_input: User message.
            ocr_text: Optional OCR text for vision agent.

        Returns:
            Agent response string.
        """
        from campusmind.agents.agent_manager import AgentManager

        self._memory.add_user(user_input)
        chat_history = self._memory.get_chat_messages()[:-1]

        try:
            mgr = AgentManager(model=self._model, temperature=self._temperature)
            agent = mgr.get_agent(agent_type)

            if agent_type == "vision":
                response = agent.run(user_input, ocr_text=ocr_text, chat_history=chat_history)
            else:
                response = agent.run(user_input, chat_history=chat_history)
        except Exception as exc:
            logger.error("Agent error (%s): %s", agent_type, exc)
            response = f"Agent error: {exc}"

        self._memory.add_ai(response)
        return response
