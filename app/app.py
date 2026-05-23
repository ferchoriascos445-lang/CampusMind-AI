"""
app.py — Application factory and bootstrap logic.
"""
from __future__ import annotations

from pathlib import Path

from config.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)


def bootstrap() -> None:
    """
    Create required directories and validate configuration on startup.
    Call this once before launching the Streamlit server.
    """
    dirs = [
        settings.UPLOADS_DIR,
        settings.OUTPUTS_DIR,
        settings.LOGS_DIR,
        settings.CHROMA_PERSIST_DIR,
        Path(settings.SQLITE_DB_PATH).parent,
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

    settings.validate()
    logger.info(
        "CampusMind AI %s bootstrap complete. Model=%s",
        settings.APP_VERSION,
        settings.DEFAULT_MODEL,
    )


def create_app():
    """
    Application factory.

    Returns:
        Configured application context (dict) ready for use.
    """
    bootstrap()
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model": settings.DEFAULT_MODEL,
    }
