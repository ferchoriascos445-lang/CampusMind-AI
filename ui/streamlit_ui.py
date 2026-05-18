"""
streamlit_ui.py — Main Streamlit application entry point.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from campusmind.app.controllers import ChatController
from campusmind.config.settings import settings
from campusmind.memory.memory_manager import MemoryManager
from campusmind.rag.rag_pipeline import RAGPipeline
from campusmind.tools.report_tool import ReportTool
from campusmind.ui.chat_interface import render_input, render_messages, render_welcome
from campusmind.ui.sidebar import render_sidebar
from campusmind.ui.upload_interface import (
    process_document_uploads,
    process_image_uploads,
    show_rag_status,
)

st.set_page_config(
    page_title="CampusMind AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp {
        background: #07080f;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,60,255,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 85% 90%, rgba(0,200,160,0.10) 0%, transparent 55%);
    }

    [data-testid="stSidebar"] {
        background: #0d0e1a !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] * { color: #c8cce0 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        font-size: 0.78rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #6b7090 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #e0e3f0 !important;
    }

    .main-header {
        background: linear-gradient(135deg,
            rgba(99,60,255,0.25) 0%,
            rgba(30,25,80,0.6) 40%,
            rgba(0,180,140,0.15) 100%);
        border: 1px solid rgba(99,60,255,0.3);
        backdrop-filter: blur(20px);
        color: white;
        padding: 1.8rem 2.2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(99,60,255,0.25), transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .main-header h1 {
        margin: 0;
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #fff 40%, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .main-header p {
        margin: 0.5rem 0 0;
        opacity: 0.65;
        font-size: 0.88rem;
        letter-spacing: 0.02em;
        -webkit-text-fill-color: rgba(255,255,255,0.65);
    }
    .main-header strong {
        -webkit-text-fill-color: #a78bfa;
        font-weight: 600;
    }

    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 14px !important;
        padding: 1rem 1.2rem !important;
        transition: border-color 0.2s;
    }
    [data-testid="metric-container"]:hover { border-color: rgba(99,60,255,0.35) !important; }
    [data-testid="metric-container"] label {
        font-size: 0.72rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #6b7090 !important;
        font-weight: 500 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Syne', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #e8eaf6 !important;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 16px !important;
        margin-bottom: 0.75rem !important;
        padding: 0.2rem 0.5rem !important;
        transition: background 0.2s;
    }
    [data-testid="stChatMessage"]:hover { background: rgba(255,255,255,0.04) !important; }
    [data-testid="stChatMessage"] p { color: #d4d7ee !important; line-height: 1.7 !important; }

    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        transition: border-color 0.2s;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(99,60,255,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,60,255,0.1) !important;
    }
    [data-testid="stChatInput"] textarea { color: #e0e3f0 !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: #4a4e6a !important; }

    hr { border-color: rgba(255,255,255,0.06) !important; margin: 1rem 0 !important; }

    .stButton > button {
        background: linear-gradient(135deg, #6336ff, #9d6ffa) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: opacity 0.2s, transform 0.15s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

    [data-testid="stDownloadButton"] > button {
        background: rgba(99,60,255,0.12) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(99,60,255,0.3) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: background 0.2s !important;
    }
    [data-testid="stDownloadButton"] > button:hover { background: rgba(99,60,255,0.22) !important; }

    .stSpinner > div { border-top-color: #6336ff !important; }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(99,60,255,0.3); border-radius: 10px; }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px dashed rgba(99,60,255,0.3) !important;
        border-radius: 14px !important;
        padding: 0.5rem !important;
    }
    [data-testid="stFileUploader"] label { color: #8b90b8 !important; }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255,80,80,0.2) !important;
        background: rgba(255,50,50,0.07) !important;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


_PDF_KEYWORDS = [
    "en pdf", "como pdf", "en formato pdf", "dame pdf", "quiero pdf",
    "genera pdf", "crea pdf", "crea un pdf", "genera un pdf",
    "archivo pdf", "documento pdf", "exportar pdf", "export pdf",
    "generate pdf", "create pdf", "save as pdf", "as pdf",
]
_WORD_KEYWORDS = [
    "en word", "como word", "en formato word", "dame word", "quiero word",
    "genera word", "crea word", "crea un word", "genera un word",
    "archivo word", "documento word", "exportar word", "en docx",
    "formato docx", "generate word", "create word", "save as word", "as word",
]


def _detect_doc_format(text: str) -> str | None:
    t = text.lower()
    if any(k in t for k in _PDF_KEYWORDS):
        return "pdf"
    if any(k in t for k in _WORD_KEYWORDS):
        return "docx"
    return None


def _init_session() -> None:
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager()
    if "rag" not in st.session_state:
        st.session_state.rag = RAGPipeline()
    if "controller" not in st.session_state:
        st.session_state.controller = ChatController(
            memory=st.session_state.memory,
            rag=st.session_state.rag,
        )
    if "report_tool" not in st.session_state:
        st.session_state.report_tool = ReportTool()
    if "last_model" not in st.session_state:
        st.session_state.last_model = settings.DEFAULT_MODEL
    if "last_temp" not in st.session_state:
        st.session_state.last_temp = settings.DEFAULT_TEMPERATURE
    if "ocr_context" not in st.session_state:
        st.session_state.ocr_context = ""


def main() -> None:
    try:
        settings.validate()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    _init_session()

    cfg = render_sidebar()

    if (
        cfg["model"] != st.session_state.last_model
        or abs(cfg["temperature"] - st.session_state.last_temp) > 0.01
    ):
        st.session_state.controller.update_model(cfg["model"], cfg["temperature"])
        st.session_state.last_model = cfg["model"]
        st.session_state.last_temp = cfg["temperature"]

    process_document_uploads(cfg["uploaded_docs"], st.session_state.rag)
    show_rag_status(st.session_state.rag)

    if cfg["uploaded_images"]:
        llm = st.session_state.controller._llm
        image_results = process_image_uploads(cfg["uploaded_images"], llm=llm)
        if image_results:
            for r in image_results:
                ocr = r.get("analysis", {}).get("ocr_text", "")
                if ocr and not ocr.startswith("["):
                    st.session_state.ocr_context += f"\n\n[{r['filename']}]\n{ocr}"

    agent_label = {
        None: "Chat general",
        "academic": "🎓 Agente académico",
        "research": "🔬 Agente investigador",
        "vision": "👁️ Agente visión",
    }.get(cfg["active_agent"], "Chat general")

    rag_badge = "✦ RAG activo" if cfg["use_rag"] else "RAG desactivado"
    docs_count = len(st.session_state.rag.ingested_files)

    st.markdown(f"""
    <div class="main-header">
        <h1>🎓 CampusMind AI</h1>
        <p>
            Modo: <strong>{agent_label}</strong> &nbsp;·&nbsp;
            Modelo: <strong>{cfg['model']}</strong> &nbsp;·&nbsp;
            <strong>{rag_badge}</strong> &nbsp;·&nbsp;
            Docs: <strong>{docs_count}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    messages = st.session_state.memory.get_display_messages()
    c1.metric("Mensajes", len(messages))
    c2.metric("Documentos", docs_count)
    c3.metric("Modelo", cfg["model"].split("/")[-1].split("-")[0].upper())
    c4.metric("Temperatura", f"{cfg['temperature']:.2f}")

    st.divider()

    if not messages:
        render_welcome()
    else:
        render_messages(messages)

    if cfg["clear_chat"]:
        st.session_state.memory.clear()
        st.session_state.ocr_context = ""
        st.rerun()

    user_input = render_input()
    if user_input:
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        doc_fmt = _detect_doc_format(user_input)

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Pensando…"):
                ctrl: ChatController = st.session_state.controller

                if cfg["active_agent"]:
                    response = ctrl.run_agent(
                        agent_type=cfg["active_agent"],
                        user_input=user_input,
                        ocr_text=st.session_state.ocr_context,
                    )
                else:
                    response = ctrl.chat(
                        user_input=user_input,
                        use_rag=cfg["use_rag"],
                    )
            st.markdown(response)

            if doc_fmt:
                mime_map = {
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                }
                doc_bytes = st.session_state.report_tool.generate_report(
                    content=response,
                    title="CampusMind AI",
                    fmt=doc_fmt,
                )
                st.download_button(
                    label=f"⬇️ Descargar .{doc_fmt}",
                    data=doc_bytes,
                    file_name=f"campusmind.{doc_fmt}",
                    mime=mime_map[doc_fmt],
                    key=f"dl_{hash(response)}",
                )

        st.rerun()


if __name__ == "__main__":
    main()