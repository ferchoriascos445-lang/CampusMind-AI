"""
sidebar.py — Streamlit sidebar: model settings, RAG toggle, file uploads.
"""
from __future__ import annotations

import streamlit as st

from campusmind.config.constants import AGENT_ACADEMIC, AGENT_RESEARCH, AGENT_VISION
from campusmind.config.settings import settings


def render_sidebar() -> dict:
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=60)
        st.title("CampusMind AI")
        st.caption("Intelligent University Assistant")
        st.divider()

        st.subheader("🤖 Model Settings")
        model = st.selectbox(
            "LLM Model",
            options=settings.AVAILABLE_MODELS,
            index=0,
            help="Switch between available models",
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=settings.DEFAULT_TEMPERATURE,
            step=0.05,
            help="Higher = more creative; lower = more precise",
        )
        st.divider()

        st.subheader("🧠 AI Agent")
        agent_labels = {
            "General Chat": None,
            "🎓 Academic Agent": AGENT_ACADEMIC,
            "🔬 Research Agent": AGENT_RESEARCH,
            "👁️ Vision Agent": AGENT_VISION,
        }
        selected_label = st.radio(
            "Active Mode",
            options=list(agent_labels.keys()),
            index=0,
            help="Select a specialised agent or use general chat",
        )
        active_agent = agent_labels[selected_label]
        st.divider()

        st.subheader("📚 Knowledge Base (RAG)")
        use_rag = st.toggle(
            "Enable RAG",
            value=False,
            help="Use uploaded documents to answer questions",
        )
        uploaded_docs = st.file_uploader(
            "Upload Documents",
            type=["pdf", "txt", "docx", "csv", "md"],
            accept_multiple_files=True,
            help="PDF, TXT, DOCX, CSV, or Markdown files",
        )
        st.divider()

        st.subheader("🖼️ Image Analysis")
        uploaded_images = st.file_uploader(
            "Upload Images",
            type=["png", "jpg", "jpeg", "bmp", "webp", "tiff"],
            accept_multiple_files=True,
            key="image_uploader",
            help="Upload images for OCR and analysis",
        )
        st.divider()

        clear_chat = st.button("🗑️ Clear Chat", use_container_width=True)

        st.divider()
        st.caption(f"v{settings.APP_VERSION} · Powered by OpenRouter")

    return {
        "model": model,
        "temperature": temperature,
        "use_rag": use_rag,
        "active_agent": active_agent,
        "uploaded_docs": uploaded_docs or [],
        "uploaded_images": uploaded_images or [],
        "clear_chat": clear_chat,
    }