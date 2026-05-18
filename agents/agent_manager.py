"""
agent_manager.py — Factory + registry for all AI agents (Factory + Observer pattern).
"""
from __future__ import annotations

from campusmind.agents.academic_agent import AcademicAgent
from campusmind.agents.research_agent import ResearchAgent
from campusmind.agents.vision_agent import VisionAgent
from campusmind.config.constants import AGENT_ACADEMIC, AGENT_RESEARCH, AGENT_VISION
from campusmind.config.logger import get_logger
from campusmind.llm.llm_factory import LLMFactory

logger = get_logger(__name__)

_AGENT_MAP = {
    AGENT_ACADEMIC: AcademicAgent,
    AGENT_RESEARCH: ResearchAgent,
    AGENT_VISION: VisionAgent,
}


class AgentManager:
    """
    Creates and caches agent instances.
    Agents share the same LLM but have distinct prompts and tools.
    """

    def __init__(
        self,
        model: str | None = None,
        temperature: float | None = None,
    ) -> None:
        self._llm = LLMFactory.create(model=model, temperature=temperature)
        self._cache: dict = {}
        logger.info("AgentManager initialised")

    def get_agent(self, agent_type: str):
        """
        Return the requested agent, creating it if necessary.

        Args:
            agent_type: One of 'academic', 'research', 'vision'.

        Returns:
            Agent instance.

        Raises:
            ValueError: For unknown agent types.
        """
        if agent_type not in _AGENT_MAP:
            raise ValueError(f"Unknown agent type: '{agent_type}'")

        if agent_type not in self._cache:
            cls = _AGENT_MAP[agent_type]
            self._cache[agent_type] = cls(self._llm)
            logger.info("Created agent: %s", agent_type)

        return self._cache[agent_type]

    @staticmethod
    def available_agents() -> list[dict]:
        """Return metadata about all available agents."""
        return [
            {
                "type": AGENT_ACADEMIC,
                "name": "Academic Agent",
                "description": "Essay help, citations, concept explanation",
            },
            {
                "type": AGENT_RESEARCH,
                "name": "Research Agent",
                "description": "Methodology, literature review, data analysis",
            },
            {
                "type": AGENT_VISION,
                "name": "Vision Agent",
                "description": "OCR interpretation and image analysis",
            },
        ]
