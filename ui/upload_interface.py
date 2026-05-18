"""
upload_interface.py — Handles document and image upload UI logic.
"""
from __future__ import annotations

import streamlit as st

from campusmind.config.logger import get_logger
from campusmind.rag.rag_pipeline import RAGPipeline
from campusmind.tools.image_tool import ImageTool

logger = get_logger(__name__)


def process_document_uploads(
    uploaded_files: list,
    rag: RAGPipeline,
    llm=None,
) -> list[str]:
    """
    Ingest uploaded documents into the RAG pipeline.

    Args:
        uploaded_files: Streamlit UploadedFile objects.
        rag: Active RAGPipeline instance.
        llm: Optional LLM for summarisation.

    Returns:
        List of ingested filenames.
    """
    if not uploaded_files:
        return []

    already_ingested = set(rag.ingested_files)
    newly_ingested = []

    for f in uploaded_files:
        if f.name in already_ingested:
            continue
        try:
            with st.spinner(f"Ingesting {f.name}…"):
                chunks = rag.ingest(f.read(), f.name)
            st.success(f"✅ {f.name} → {chunks} chunks indexed")
            newly_ingested.append(f.name)
            logger.info("Ingested document: %s", f.name)
        except Exception as exc:
            st.error(f"❌ Failed to ingest {f.name}: {exc}")
            logger.error("Ingest error for %s: %s", f.name, exc)

    return newly_ingested


def process_image_uploads(uploaded_images: list, llm=None) -> list[dict]:
    """
    Run OCR and analysis on uploaded images.

    Args:
        uploaded_images: Streamlit UploadedFile image objects.
        llm: Optional LLM for enriched captioning.

    Returns:
        List of analysis result dicts.
    """
    if not uploaded_images:
        return []

    tool = ImageTool()
    results = []

    for img_file in uploaded_images:
        try:
            img_bytes = img_file.read()
            with st.spinner(f"Analysing {img_file.name}…"):
                analysis = tool.analyze(img_bytes)
                caption = tool.caption(img_bytes, llm=llm)

            with st.expander(f"🖼️ {img_file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img_bytes, use_container_width=True)
                with col2:
                    info = analysis.get("info", {})
                    st.markdown(f"**Size:** {info.get('width')}×{info.get('height')} px")
                    st.markdown(f"**Format:** {info.get('format', 'unknown')}")
                    st.markdown(f"**Description:** {caption}")

                    ocr_text = analysis.get("ocr_text", "")
                    if ocr_text and not ocr_text.startswith("["):
                        st.markdown("**OCR Text:**")
                        st.text_area(
                            label="",
                            value=ocr_text,
                            height=120,
                            key=f"ocr_{img_file.name}",
                        )

            results.append({
                "filename": img_file.name,
                "analysis": analysis,
                "caption": caption,
            })
        except Exception as exc:
            st.error(f"❌ Image analysis failed for {img_file.name}: {exc}")
            logger.error("Image analysis error: %s", exc)

    return results


def show_rag_status(rag: RAGPipeline) -> None:
    """Display the current RAG knowledge base status."""
    files = rag.ingested_files
    if files:
        st.sidebar.markdown("**Indexed documents:**")
        for f in files:
            st.sidebar.markdown(f"- 📄 {f}")
    else:
        st.sidebar.caption("No documents indexed yet.")
