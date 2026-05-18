# CampusMind AI 🎓

**An intelligent multimodal university assistant powered by Groq LLMs, LangChain, and ChromaDB.**

---

## What It Does

CampusMind AI is a private, enterprise-grade AI assistant for universities. It provides:

| Feature | Description |
|---|---|
| 💬 **LLM Chat** | Conversational AI with persistent memory |
| 📚 **RAG** | Document Q&A over PDF, DOCX, TXT, CSV |
| 🎓 **Academic Agent** | Essay help, citations, concept explanations |
| 🔬 **Research Agent** | Methodology, literature review, data analysis |
| 👁️ **Vision Agent** | OCR extraction and image analysis |
| 💾 **Export** | Download chats as PDF, DOCX, TXT, or Markdown |

---

## Quick Start

### 1. Set your API key

```bash
export GROQ_API_KEY=your_key_here
```

Get a free key at https://console.groq.com

### 2. Install dependencies

```bash
pip install -r campusmind/requirements.txt
```

### 3. Launch

```bash
python -m streamlit run campusmind/ui/streamlit_ui.py \
  --server.port 8080 --server.address 0.0.0.0 --server.headless true
```

---

## Architecture

```
campusmind/
├── app/           ← Bootstrap, routes, controllers
├── llm/           ← Groq client, LLM factory, prompts, chains
├── rag/           ← Document loader, splitter, retriever, pipeline
├── embeddings/    ← Embedding manager (HuggingFace / ChromaDB default)
├── vectorstore/   ← ChromaDB manager, vector factory
├── agents/        ← Academic, Research, Vision agents + manager
├── memory/        ← ChatMemory (in-session) + PersistentMemory (SQLite)
├── tools/         ← OCR, image, document, report, search tools
├── vision/        ← OCR engine, image analysis, captioning
├── ui/            ← Streamlit sidebar, chat, upload interfaces
├── config/        ← Settings (env vars), constants, logger
├── database/      ← SQLite manager for history persistence
├── tests/         ← Smoke tests
└── main.py        ← Entry point
```

### Design Patterns Used

- **Singleton** — `GroqClient`, `EmbeddingManager`, `ChromaManager`
- **Factory** — `LLMFactory`, `VectorStoreFactory`, `AgentManager`
- **Strategy** — Swappable LLM backends, vector store backends
- **Adapter** — `OCRTool`, `ImageTool`, `SearchTool` wrap domain objects
- **Observer** — `PersistentMemory` listens to conversation events
- **Facade** — `MemoryManager`, `RAGPipeline` unify complex subsystems
- **LCEL Chains** — LangChain Expression Language for composable pipelines

---

## RAG System

**Ingest path:**
```
File upload → DocumentLoader → DocumentSplitter → EmbeddingManager → ChromaDB
```

**Query path:**
```
User query → DocumentRetriever → format_context → RAG chain (Groq LLM) → Response
```

Supported file types: `PDF`, `TXT`, `DOCX`, `CSV`, `MD`

---

## Available LLM Models (Groq)

| Model | Context | Best For |
|---|---|---|
| `llama3-70b-8192` | 8K tokens | General tasks, reasoning |
| `mixtral-8x7b-32768` | 32K tokens | Long documents, analysis |
| `llama3-8b-8192` | 8K tokens | Fast responses |

---

## Agents

### AcademicAgent
Specialised in: essay structure, APA/MLA/Chicago citations, subject-matter Q&A, concept explanations.

### ResearchAgent
Specialised in: research methodology, hypothesis design, literature synthesis, statistical interpretation.

### VisionAgent
Specialised in: interpreting OCR output, describing image content, analysing extracted text.

---

## Memory System

- **In-session**: `ChatMessageHistory` (LangChain) — fast, in-memory
- **Persistent**: SQLite via `SQLiteManager` — survives restarts
- **Session recovery**: Past conversations recoverable by session ID

---

## Export Formats

| Format | Library |
|---|---|
| PDF | reportlab |
| DOCX | python-docx |
| TXT | built-in |
| Markdown | built-in |

---

## Configuration (`.env`)

```env
GROQ_API_KEY=your_key
DEFAULT_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

Copy `.env.example` to `.env` and fill in your values.

---

## Docker

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8080`.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `GROQ_API_KEY not set` | Add key to `.env` or environment secrets |
| ChromaDB slow first run | Embeddings download on first use |
| OCR not working | Install tesseract: `apt install tesseract-ocr` |
| Disk quota error | Skip `faiss-cpu` and `sentence-transformers` |

---

## Tech Stack

- **LLM**: Groq (llama3-70b, mixtral-8x7b)
- **Orchestration**: LangChain + LCEL
- **Vector DB**: ChromaDB
- **UI**: Streamlit
- **DB**: SQLite (via SQLAlchemy-compatible manager)
- **Documents**: pypdf, python-docx, reportlab
- **Vision**: Pillow, pytesseract (optional)
