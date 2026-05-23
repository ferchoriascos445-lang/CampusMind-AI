"""
chat_interface.py — Renders the chat message history and input box.
"""
from __future__ import annotations
import re
import streamlit as st


def _render_content(content: str) -> None:
    """
    Renderiza el contenido de un mensaje detectando bloques LaTeX y texto normal.
    
    Soporta:
    - Bloques LaTeX: $$...$$  o  \\[...\\]
    - Inline LaTeX: $...$  o  \\(...\\)
    - Texto markdown normal
    """
    # Separar por bloques LaTeX de bloque ($$...$$)
    parts = re.split(r'(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\])', content)
    
    for part in parts:
        if not part.strip():
            continue
        
        # Bloque LaTeX $$...$$ o \[...\]
        if (part.startswith('$$') and part.endswith('$$')):
            formula = part[2:-2].strip()
            st.latex(formula)
        elif (part.startswith('\\[') and part.endswith('\\]')):
            formula = part[2:-2].strip()
            st.latex(formula)
        else:
            # Dentro del texto normal, buscar inline LaTeX $...$ o \(...\)
            # y renderizar mezclando markdown con st.latex
            inline_parts = re.split(r'(\$[^$\n]+?\$|\\\([\s\S]*?\\\))', part)
            
            has_inline = any(
                (p.startswith('$') and p.endswith('$') and len(p) > 2) or
                (p.startswith('\\(') and p.endswith('\\)'))
                for p in inline_parts
            )
            
            if has_inline:
                for ip in inline_parts:
                    if not ip:
                        continue
                    if ip.startswith('$') and ip.endswith('$') and len(ip) > 2:
                        formula = ip[1:-1].strip()
                        st.latex(formula)
                    elif ip.startswith('\\(') and ip.endswith('\\)'):
                        formula = ip[2:-2].strip()
                        st.latex(formula)
                    elif ip.strip():
                        st.markdown(ip)
            else:
                st.markdown(part)


def render_messages(messages: list[dict]) -> None:
    for msg in messages:
        role = msg["role"]
        avatar = "🎓" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            _render_content(msg["content"])


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