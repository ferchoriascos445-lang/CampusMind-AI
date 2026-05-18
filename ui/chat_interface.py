"""
chat_interface.py — Renders the chat message history and input box.
"""
from __future__ import annotations

import streamlit as st


def render_messages(messages: list[dict]) -> None:
    for msg in messages:
        role = msg["role"]
        avatar = "🎓" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])


def render_input() -> str | None:
    return st.chat_input("Ask CampusMind AI anything…")


def render_welcome() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding: 3rem 1rem;">
            <img src="https://img.icons8.com/fluency/96/graduation-cap.png" width="80"/>
            <h2 style="margin-top:1rem;">Welcome to CampusMind AI</h2>
            <p style="color:gray; font-size:1.1rem;">
                Your intelligent university assistant powered by OpenRouter.<br>
                Ask questions, upload documents, analyse images, or choose a specialised agent from the sidebar.
            </p>
            <hr style="margin: 2rem auto; width: 60%;"/>
            <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; color:gray;">
                <div>💬 <strong>General Chat</strong><br>Conversational AI</div>
                <div>📚 <strong>RAG</strong><br>Document Q&A</div>
                <div>🎓 <strong>Academic</strong><br>Writing & Citations</div>
                <div>🔬 <strong>Research</strong><br>Methodology</div>
                <div>👁️ <strong>Vision</strong><br>OCR & Image Analysis</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )