"""
upload_interface.py — Handles document and image upload UI logic.
"""
from __future__ import annotations
 
import streamlit as st
 
from config.logger import get_logger
from rag.rag_pipeline import RAGPipeline
from tools.image_tool import ImageTool
 
logger = get_logger(__name__)
 
 
def process_document_uploads(
    uploaded_files: list,
    rag: RAGPipeline,
    llm=None,
) -> list[str]:
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
    Procesa imágenes subidas: guarda bytes en session_state y muestra preview.
    
    FIX: Lee los bytes UNA sola vez y los guarda en session_state.image_bytes
    para que el VisionAgent pueda usarlos aunque el file_uploader se resetee.
    """
    if not uploaded_images:
        return []
 
    tool = ImageTool()
    results = []
 
    for img_file in uploaded_images:
        try:
            # FIX: leer bytes una sola vez y guardarlos
            img_bytes = img_file.read()
            
            # Guardar en session_state indexado por nombre de archivo
            if "image_store" not in st.session_state:
                st.session_state.image_store = {}
            st.session_state.image_store[img_file.name] = img_bytes
            # También guardar el último como image_bytes para compatibilidad
            st.session_state.image_bytes = img_bytes
            st.session_state.image_filename = img_file.name
 
            with st.spinner(f"Analizando {img_file.name}…"):
                analysis = tool.analyze(img_bytes)
                caption = tool.caption(img_bytes, llm=llm)
 
            with st.expander(f"🖼️ {img_file.name}", expanded=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img_bytes, use_container_width=True)
                with col2:
                    info = analysis.get("info", {})
                    st.markdown(f"**Tamaño:** {info.get('width')}×{info.get('height')} px")
                    st.markdown(f"**Formato:** {info.get('format', 'desconocido')}")
                    st.markdown(f"**Descripción:** {caption}")
 
                    ocr_text = analysis.get("ocr_text", "")
                    if ocr_text and not ocr_text.startswith("["):
                        st.markdown("**Texto OCR:**")
                        st.text_area(
                            label="",
                            value=ocr_text,
                            height=120,
                            key=f"ocr_{img_file.name}_{id(img_bytes)}",
                        )
                    
                    # Indicar si el modelo actual soporta visión
                    if llm:
                        model_name = getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""
                        vision_models = ["gpt-4o", "claude-3", "gemini", "llama-3.2"]
                        supports = any(v in model_name.lower() for v in vision_models)
                        if supports:
                            st.success("✅ Modelo con visión activo — análisis directo disponible")
                        else:
                            st.warning(
                                f"⚠️ `{model_name}` no soporta visión directa. "
                                "Cambia a `openai/gpt-4o-mini` para mejor análisis de imágenes."
                            )
 
            results.append({
                "filename": img_file.name,
                "analysis": analysis,
                "caption": caption,
                "image_bytes": img_bytes,
            })
 
        except Exception as exc:
            st.error(f"❌ Error al analizar {img_file.name}: {exc}")
            logger.error("Image analysis error: %s", exc)
 
    return results
 
 
def show_rag_status(rag: RAGPipeline) -> None:
    files = rag.ingested_files
    if files:
        st.sidebar.markdown("**Documentos indexados:**")
        for f in files:
            st.sidebar.markdown(f"- 📄 {f}")
    else:
        st.sidebar.caption("No hay documentos indexados.")