"""
test_smoke.py — Basic smoke tests (no API calls, no heavy deps required).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_settings_import():
    from campusmind.config.settings import settings
    assert settings.APP_NAME == "CampusMind AI"
    assert settings.APP_VERSION == "1.0.0"


def test_constants_import():
    from campusmind.config.constants import AGENT_ACADEMIC, AGENT_RESEARCH, AGENT_VISION
    assert AGENT_ACADEMIC == "academic"
    assert AGENT_RESEARCH == "research"
    assert AGENT_VISION == "vision"


def test_document_loader_txt():
    from campusmind.rag.document_loader import DocumentLoader
    docs = DocumentLoader.load_from_bytes(b"Hello university world!", "test.txt")
    assert len(docs) == 1
    assert "Hello university world!" in docs[0].page_content


def test_document_loader_csv():
    from campusmind.rag.document_loader import DocumentLoader
    csv_data = b"name,grade\nAlice,A\nBob,B"
    docs = DocumentLoader.load_from_bytes(csv_data, "grades.csv")
    assert len(docs) == 2


def test_splitter():
    from langchain_core.documents import Document
    from campusmind.rag.splitter import DocumentSplitter
    long_text = "word " * 500
    docs = [Document(page_content=long_text, metadata={"source": "test"})]
    splitter = DocumentSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split(docs)
    assert len(chunks) > 1


def test_report_tool_txt():
    from campusmind.tools.report_tool import ReportTool
    tool = ReportTool()
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
    data = tool.export_chat(messages, fmt="txt", title="Test Export")
    assert b"Hello" in data
    assert b"Hi there!" in data


def test_routes():
    from campusmind.app.routes import resolve
    assert resolve("/chat") == "chat"
    assert resolve("/unknown") == "chat"


def test_agent_manager_metadata():
    from campusmind.agents.agent_manager import AgentManager
    agents = AgentManager.available_agents()
    assert len(agents) == 3
    types = [a["type"] for a in agents]
    assert "academic" in types
    assert "research" in types
    assert "vision" in types
