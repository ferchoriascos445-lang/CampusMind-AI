"""
constants.py — Application-wide constants.
"""

# Supported file types for document upload
SUPPORTED_DOC_TYPES = ["pdf", "txt", "docx", "csv", "md"]
SUPPORTED_IMAGE_TYPES = ["png", "jpg", "jpeg", "bmp", "tiff", "webp"]

# Vector store backend options
VECTOR_BACKEND_CHROMA = "chroma"
VECTOR_BACKEND_FAISS = "faiss"

# Agent types
AGENT_ACADEMIC = "academic"
AGENT_RESEARCH = "research"
AGENT_VISION = "vision"

# Memory types
MEMORY_BUFFER = "buffer"
MEMORY_SUMMARY = "summary"

# Streamlit session keys
SESSION_MESSAGES = "messages"
SESSION_MEMORY = "memory"
SESSION_VECTOR_STORE = "vector_store"
SESSION_AGENT = "agent"
SESSION_HISTORY_ID = "history_id"

# OCR languages
OCR_LANG_DEFAULT = "eng"
OCR_LANG_SPANISH = "spa"
OCR_LANG_MULTI = "eng+spa"

# Document export formats
EXPORT_PDF = "pdf"
EXPORT_DOCX = "docx"
EXPORT_TXT = "txt"
EXPORT_MD = "md"

# System prompt tokens to reserve
SYSTEM_PROMPT_RESERVE = 500

# UI
MAX_DISPLAY_MESSAGES = 100
