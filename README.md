<div align="center">

# 🎓 CampusMind AI

**Asistente universitario inteligente con IA multimodal**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1.0%2B-1C3D5A?logo=chainlink&logoColor=white)](https://langchain.com)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-6336FF)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

*Chatea con tus documentos, analiza imágenes y genera reportes académicos con IA — todo desde una sola interfaz web.*

</div>

---

## ✨ Características principales

| Funcionalidad | Descripción |
|---|---|
| 💬 **Chat con IA** | Conversación en lenguaje natural con modelos LLaMA, Mistral y GPT-4o |
| 📚 **RAG — Document Q&A** | Sube PDFs, Word, CSV o TXT y hazles preguntas directamente |
| 🎓 **Agente Académico** | Redacción de ensayos, citas APA/MLA/Chicago, explicación de conceptos |
| 🔬 **Agente de Investigación** | Diseño metodológico, análisis estadístico, literatura científica |
| 👁️ **Agente de Visión** | Análisis de imágenes, OCR y resolución de ecuaciones matemáticas |
| 📄 **Exportación** | Genera reportes en PDF y Word con fórmulas LaTeX renderizadas |
| 🔁 **Multi-modelo** | Cambia de modelo LLM en tiempo real desde la barra lateral |
| 💾 **Historial persistente** | Las conversaciones se guardan en SQLite entre sesiones |

---

## 🏗️ Arquitectura

```
CampusMind AI
├── ui/                     # Interfaz Streamlit
│   ├── streamlit_ui.py     # Punto de entrada principal
│   ├── sidebar.py          # Panel lateral (modelos, agentes, RAG)
│   ├── chat_interface.py   # Renderizado de mensajes y LaTeX
│   └── upload_interface.py # Carga y procesamiento de archivos
│
├── app/
│   └── controllers.py      # Lógica de negocio (chat, RAG, agentes)
│
├── agents/
│   ├── agent_manager.py    # Factory de agentes
│   ├── academic_agent.py   # Agente académico
│   ├── research_agent.py   # Agente de investigación
│   └── vision_agent.py     # Agente de visión multimodal
│
├── llm/
│   ├── llm_factory.py      # Factory pattern para el LLM
│   ├── openrouter_client.py# Cliente OpenRouter (Singleton + reintentos)
│   ├── chains.py           # Cadenas LCEL
│   └── prompts.py          # Plantillas de prompts centralizadas
│
├── rag/
│   └── rag_pipeline.py     # Pipeline RAG completo
│
├── embeddings/
│   └── embedding_manager.py# Gestor de embeddings (Singleton)
│
├── vectorstore/
│   └── chroma_manager.py   # ChromaDB manager
│
├── memory/
│   └── memory_manager.py   # Memoria de conversación
│
├── database/
│   └── sqlite_manager.py   # Persistencia SQLite
│
├── vision/
│   ├── image_analysis.py   # Análisis técnico de imágenes
│   ├── image_captioning.py # Generación de descripciones
│   └── ocr_engine.py       # Extracción de texto (tesseract)
│
├── tools/
│   ├── report_tool.py      # Exportación PDF/DOCX con LaTeX
│   └── image_tool.py       # Herramienta de análisis visual
│
└── config/
    ├── settings.py         # Configuración centralizada (.env)
    └── logger.py           # Logger estructurado
```

---

## 🚀 Instalación rápida

### Requisitos previos

- Python 3.10 o superior
- Cuenta en [OpenRouter](https://openrouter.ai) (tiene modelos gratuitos)
- *(Opcional)* [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) para extracción de texto en imágenes

### 1. Clonar el repositorio

```bash
https://github.com/ferchoriascos445-lang/CampusMind-AI.git
cd CampusMind-AI
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv --without-pip
venv\Scripts\activate
python -m ensurepip

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

# Para soporte de fórmulas LaTeX en documentos exportados
pip install matplotlib

# Para OCR en imágenes (opcional)
pip install pytesseract
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Obligatorio — obtén tu clave en https://openrouter.ai/keys
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Opcionales — tienen valores por defecto
DEFAULT_MODEL=meta-llama/llama-3.1-8b-instruct:free
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4096
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

### 5. Lanzar la aplicación

```bash
# Windows
$env:PYTHONPATH = $PWD
streamlit run ui\streamlit_ui.py --server.port 8080

# macOS / Linux
PYTHONPATH=. streamlit run ui/streamlit_ui.py --server.port 8080
```

Abre tu navegador en **http://localhost:8080**

---

## 🐳 Despliegue con Docker

```bash
# Construir y levantar
docker-compose up --build

# En segundo plano
docker-compose up -d
```

La aplicación estará disponible en **http://localhost:8080**

> ℹ️ Agrega `OPENAI_API_KEY=tu_clave` en el archivo `docker-compose.yml` o en un archivo `.env` antes de levantar el contenedor.

---

## 🧠 Modelos LLM disponibles

| Modelo | Proveedor | Visión | Costo |
|---|---|---|---|
| `meta-llama/llama-3.1-8b-instruct:free` | Meta AI | ❌ | Gratis |
| `mistralai/mistral-7b-instruct:free` | Mistral AI | ❌ | Gratis |
| `meta-llama/llama-3.2-11b-vision-instruct` | Meta AI | ✅ | Bajo |
| `meta-llama/llama-3.1-70b-instruct` | Meta AI | ❌ | Medio |
| `openai/gpt-4o-mini` | OpenAI | ✅ | Medio |

> 💡 Para análisis de imágenes usa `openai/gpt-4o-mini` o `llama-3.2-11b-vision-instruct`. El resto de los agentes funcionan con cualquier modelo.

---

## 📖 Cómo usar

### Chat con documentos (RAG)

1. Activa **Enable RAG** en la barra lateral
2. Sube un documento en **Upload Documents** (PDF, Word, CSV, TXT)
3. Escribe tu pregunta — el sistema busca en el documento antes de responder

### Agentes especializados

Selecciona el agente desde la barra lateral:

- **Academic Agent** — *"Escribe un ensayo sobre la inteligencia artificial con citas APA"*
- **Research Agent** — *"Diseña la metodología para una investigación cuantitativa sobre..."*
- **Vision Agent** — Sube una imagen y pregunta *"¿Qué ecuaciones aparecen en esta imagen?"*

### Exportar documentos

Agrega `en PDF` o `en Word` a cualquier solicitud:

```
Escribe un resumen de métodos numéricos con sus fórmulas en LaTeX en PDF
```

El archivo aparecerá con un botón de descarga directamente en el chat.

---

## ⚙️ Configuración avanzada

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `DEFAULT_MODEL` | `llama-3.1-8b-instruct:free` | Modelo LLM inicial |
| `DEFAULT_TEMPERATURE` | `0.7` | Creatividad del modelo (0.0–1.0) |
| `MAX_TOKENS` | `4096` | Máximo de tokens por respuesta |
| `CHUNK_SIZE` | `1000` | Tamaño de fragmentos para RAG |
| `CHUNK_OVERLAP` | `200` | Solapamiento entre fragmentos |
| `RETRIEVAL_K` | `4` | Número de fragmentos recuperados |
| `CHROMA_PERSIST_DIR` | `./campusmind_data/chroma` | Directorio de ChromaDB |
| `SQLITE_DB_PATH` | `./campusmind_data/history.db` | Base de datos de historial |

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Interfaz web | Streamlit ≥ 1.35 |
| Orquestación IA | LangChain ≥ 1.0 + LCEL |
| Proveedor LLM | OpenRouter API |
| Base vectorial | ChromaDB ≥ 0.5 |
| Embeddings | all-MiniLM-L6-v2 (SentenceTransformers) |
| Persistencia | SQLite 3 |
| Exportación | reportlab + python-docx |
| Fórmulas LaTeX | matplotlib |
| Visión / OCR | Pillow + pytesseract |
| Resiliencia | tenacity ≥ 8.2 |
| Contenedor | Docker + Docker Compose |

---

## 🎨 Patrones de diseño

- **Singleton** — `OpenRouterClient` y `EmbeddingManager`
- **Factory** — `LLMFactory` y `AgentManager`
- **Strategy** — intercambio de modelo LLM en tiempo de ejecución
- **Facade** — `RAGPipeline` y `MemoryManager`
- **Observer** — memoria persistente de conversación
- **Adapter** — herramientas OCR y búsqueda con interfaz uniforme

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m "feat: descripción"`
4. Sube tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

<div align="center">

Desarrollado por **Carlos Fernando Paredes Riascos**  
Universidad Cooperativa de Colombia · 2026

</div>
