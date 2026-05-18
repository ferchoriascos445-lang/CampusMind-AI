"""
routes.py — Route definitions mapping paths to controllers.
(Used programmatically; Streamlit handles routing via UI components.)
"""
from __future__ import annotations

from campusmind.config.logger import get_logger

logger = get_logger(__name__)

ROUTES = {
    "/": "chat",
    "/chat": "chat",
    "/rag": "rag",
    "/agents": "agents",
    "/vision": "vision",
    "/export": "export",
    "/history": "history",
}


def resolve(path: str) -> str:
    """
    Resolve a URL path to a controller action name.

    Args:
        path: URL path string.

    Returns:
        Action name string, defaults to 'chat'.
    """
    action = ROUTES.get(path, "chat")
    logger.debug("Route %s → %s", path, action)
    return action
