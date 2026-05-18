"""
report_tool.py — Generates PDF, DOCX, TXT, and Markdown export files.
"""
from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

from campusmind.config.logger import get_logger
from campusmind.config.settings import settings

logger = get_logger(__name__)


class ReportTool:
    """
    Generates downloadable reports from chat history or arbitrary text.
    Supports: PDF (reportlab), DOCX (python-docx), TXT, Markdown.
    """

    def __init__(self) -> None:
        output_dir = Path(settings.OUTPUTS_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        self._output_dir = output_dir

    def export_chat(
        self,
        messages: list[dict],
        fmt: str = "txt",
        title: str = "Chat Export",
    ) -> bytes:
        """
        Export chat history to the requested format.

        Args:
            messages: List of {'role': ..., 'content': ...} dicts.
            fmt: Export format ('pdf', 'docx', 'txt', 'md').
            title: Document title.

        Returns:
            File bytes ready for download.
        """
        text_lines = []
        for m in messages:
            role = "You" if m["role"] == "user" else "CampusMind AI"
            text_lines.append(f"{role}:\n{m['content']}\n")
        full_text = "\n".join(text_lines)

        dispatch = {
            "pdf": self._to_pdf,
            "docx": self._to_docx,
            "txt": self._to_txt,
            "md": self._to_md,
        }
        fn = dispatch.get(fmt, self._to_txt)
        return fn(full_text, title)

    def generate_report(self, content: str, title: str, fmt: str = "pdf") -> bytes:
        """Generate a standalone report document."""
        dispatch = {
            "pdf": self._to_pdf,
            "docx": self._to_docx,
            "txt": self._to_txt,
            "md": self._to_md,
        }
        fn = dispatch.get(fmt, self._to_txt)
        return fn(content, title)

    # ── Format implementations ─────────────────────────────────────────────────

    @staticmethod
    def _to_pdf(text: str, title: str) -> bytes:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import cm
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            story = [
                Paragraph(title, styles["Title"]),
                Spacer(1, 0.5*cm),
                Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"), styles["Normal"]),
                Spacer(1, 0.5*cm),
            ]
            for line in text.split("\n"):
                if line.strip():
                    story.append(Paragraph(line, styles["Normal"]))
                    story.append(Spacer(1, 0.2*cm))
            doc.build(story)
            logger.info("PDF generated: %d bytes", buf.tell())
            return buf.getvalue()
        except Exception as exc:
            logger.error("PDF generation error: %s", exc)
            return text.encode()

    @staticmethod
    def _to_docx(text: str, title: str) -> bytes:
        try:
            from docx import Document
            from docx.shared import Pt

            doc = Document()
            doc.add_heading(title, level=1)
            doc.add_paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"))
            doc.add_paragraph("")
            for line in text.split("\n"):
                doc.add_paragraph(line)
            buf = io.BytesIO()
            doc.save(buf)
            logger.info("DOCX generated")
            return buf.getvalue()
        except Exception as exc:
            logger.error("DOCX generation error: %s", exc)
            return text.encode()

    @staticmethod
    def _to_txt(text: str, title: str) -> bytes:
        header = f"{title}\n{'='*len(title)}\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        return (header + text).encode("utf-8")

    @staticmethod
    def _to_md(text: str, title: str) -> bytes:
        header = f"# {title}\n\n_{datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
        return (header + text).encode("utf-8")
