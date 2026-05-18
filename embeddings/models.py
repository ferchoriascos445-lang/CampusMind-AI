"""
models.py — Registry of available embedding model configurations.
"""
from __future__ import annotations

EMBEDDING_MODELS = {
    "all-MiniLM-L6-v2": {
        "name": "all-MiniLM-L6-v2",
        "dimensions": 384,
        "description": "Fast, lightweight sentence embeddings (default)",
        "provider": "huggingface",
    },
    "all-mpnet-base-v2": {
        "name": "all-mpnet-base-v2",
        "dimensions": 768,
        "description": "Higher quality sentence embeddings",
        "provider": "huggingface",
    },
    "chroma-default": {
        "name": "chroma-default",
        "dimensions": 384,
        "description": "ChromaDB built-in embeddings (no download required)",
        "provider": "chroma",
    },
}


def get_model_info(name: str) -> dict:
    """Return metadata for a named embedding model."""
    return EMBEDDING_MODELS.get(name, EMBEDDING_MODELS["chroma-default"])


def list_models() -> list[dict]:
    """Return all available embedding model configurations."""
    return list(EMBEDDING_MODELS.values())
