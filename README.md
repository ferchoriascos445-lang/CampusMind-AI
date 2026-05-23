# CampusMind AI 🎓

**An intelligent multimodal university assistant powered by OpenRouter, OpenAI models, LangChain, and ChromaDB.**

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

# Features

- Multi-agent AI architecture
- Retrieval-Augmented Generation (RAG)
- Persistent memory with SQLite
- OCR and image understanding
- Multimodal AI assistant
- Vector search using ChromaDB
- Streamlit web interface
- PDF, DOCX, TXT, and Markdown export
- Modular and scalable architecture
- Enterprise-grade design patterns

---

## Quick Start

### 1. Clone repository

```bash
git clone https://github.com/ferchoriascos445-lang/CampusMind-AI.git
cd CampusMind-AI
```

---

### 2. Create virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_api_key
DEFAULT_MODEL=openai/gpt-4o
DEFAULT_TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

Get your API key from:

https://openrouter.ai

---

### 5. Launch application

```bash
streamlit run campusmind/ui/streamlit_ui.py \
--server.port 8080 \
--server.address 0.0.0.0 \
--server.headless true
```

Open in browser:

```text
http://localhost:8080
```

---

# System Architecture

```text
campusmind/
├── app/               # Bootstrap, routes, controllers
├── llm/               # OpenRouter client, prompts, chains
├── rag/               # RAG pipeline and retrievers
├── embeddings/        # Embedding manager
├── vectorstore/       # ChromaDB integration
├── agents/            # Academic, Research, Vision agents
├── memory/            # Persistent and session memory
├── tools/             # OCR, image, search, reports
├── vision/            # OCR and image processing
├── ui/                # Streamlit interface
├── config/            # Settings and logger
├── database/          # SQLite manager
├── tests/             # Unit and smoke tests
└── main.py            # Application entry point
```

---

# Design Patterns Used

| Pattern | Usage |
|---|---|
| Singleton | OpenRouter client, embedding manager |
| Factory | LLM and vector store creation |
| Strategy | Swappable LLM providers |
| Adapter | OCR and search tool wrappers |
| Observer | Persistent memory event listeners |
| Facade | MemoryManager and RAGPipeline |
| LCEL | LangChain composable chains |

---

# RAG Pipeline

## Document Ingestion

```text
File Upload
   ↓
Document Loader
   ↓
Document Splitter
   ↓
Embedding Manager
   ↓
ChromaDB Vector Store
```

---

## Query Flow

```text
User Question
   ↓
Retriever
   ↓
Context Formatter
   ↓
LLM Chain
   ↓
AI Response
```

---

# Supported File Types

- PDF
- DOCX
- TXT
- CSV
- Markdown

---

# Available Models

| Model | Provider | Best Use |
|---|---|---|
| openai/gpt-4o | OpenAI | Multimodal reasoning |
| openai/gpt-4.1 | OpenAI | Coding and analysis |
| openai/gpt-4.1-mini | OpenAI | Fast responses |
| openai/gpt-3.5-turbo | OpenAI | Lightweight tasks |

---

# Agents

## AcademicAgent

Capabilities:

- Essay generation
- Citation formatting
- Concept explanations
- Subject tutoring

---

## ResearchAgent

Capabilities:

- Research methodologies
- Literature review synthesis
- Statistical interpretation
- Hypothesis generation

---

## VisionAgent

Capabilities:

- OCR extraction
- Image understanding
- Screenshot analysis
- Multimodal reasoning

---

# Memory System

| Type | Description |
|---|---|
| Session Memory | LangChain ChatMessageHistory |
| Persistent Memory | SQLite database |
| Session Recovery | Restore previous conversations |

---

# Export Formats

| Format | Library |
|---|---|
| PDF | reportlab |
| DOCX | python-docx |
| TXT | built-in |
| Markdown | built-in |

---

# Tech Stack

| Technology | Usage |
|---|---|
| OpenRouter | LLM provider |
| OpenAI Models | GPT-4o, GPT-4.1 |
| LangChain | AI orchestration |
| LCEL | Chain composition |
| ChromaDB | Vector database |
| SQLite | Persistent memory |
| Streamlit | Web UI |
| Pillow | Image processing |
| pytesseract | OCR |
| reportlab | PDF generation |

---

# Docker Support

## Build and run

```bash
docker-compose up --build
```

---

# Troubleshooting

| Issue | Solution |
|---|---|
| OPENROUTER_API_KEY not set | Configure `.env` correctly |
| OCR not working | Install `tesseract-ocr` |
| Slow first startup | Embeddings download initially |
| Streamlit not found | Activate virtual environment |

---

# Security Notes

- Never upload `.env`
- Always add `.env` to `.gitignore`
- Rotate exposed API keys immediately
- Use environment variables for secrets

---

# Future Improvements

- Multi-user authentication
- Voice assistant support
- Fine-tuned university models
- Advanced analytics dashboard
- Hybrid vector databases
- Real-time collaboration
- Agent orchestration system

---

# License

MIT License

---

# Author

Carlos Fernando Paredes Riascos

---

# Screenshots

_Add application screenshots here_

---

# Contributing

Pull requests and contributions are welcome.

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request

---

# Acknowledgments

- OpenRouter
- OpenAI
- LangChain
- ChromaDB
- Streamlit
- Python community
