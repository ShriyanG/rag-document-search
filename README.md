# RAG Document Search

A modular, production-style **Retrieval-Augmented Generation (RAG)** system for querying private PDF documents using dense retrieval and large language models.

This project is designed to mirror real-world ML systems rather than notebook-only prototypes. It emphasizes **clean architecture**, **token-aware retrieval**, and **reproducible pipelines**.

---

## ✨ Features

* End-to-end RAG pipeline: **ingestion → embedding → indexing → retrieval → generation**
* Token-aware retrieval that dynamically adapts context size to model limits
* Local LLM support (CPU-friendly) with pluggable backends
* FAISS-based vector search for efficient similarity retrieval
* Clean, subcommand-based CLI for pipeline setup and querying
* Modular codebase structured for extensibility and experimentation

---

## 🏗️ Project Architecture

```
src/
├── main.py                # CLI entry point
├── rag.py                 # RAG orchestration logic
│
├── components/
│   ├── llm/               # LLM abstractions (Local, OpenAI, etc.)
│   └── data/              # Data ingestion (PDF parsing)
│
├── retrieval/
│   ├── embeddings.py      # Embedding generation
│   ├── indexing.py        # FAISS index construction
│   └── retrieve.py        # Similarity search
│
├── utils/                 # Token estimation, helpers
└── config.py              # Model and system configuration
```

The pipeline stages are intentionally decoupled to allow incremental rebuilding and easier debugging.

---

## 🚀 Getting Started

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional - For OpenAI Models)

The system supports **two types of LLMs**:

#### Local Models (No API Key Required)
Default models like `google/flan-t5-small` run entirely locally and require no API key.

#### OpenAI Models (API Key Required)
To use GPT models (`gpt-3.5-turbo`, `gpt-4`, etc.), you'll need an OpenAI API key:

1. **Get API Key**: Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. **Set Environment Variable**:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Or create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
# Edit .env and add your API key
```

To make it persistent across terminal sessions, add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

---

## 🧠 LLM Management

The system supports **easy switching between local and OpenAI models** without code changes.

### List Available Models

```bash
python src/main.py list-llms
```

Output:
```
📚 Supported LLM Models:

  LOCAL:
    - google/flan-t5-small
    - google/flan-t5-base
    - google/flan-t5-large
    - google/flan-t5-xl
    - gpt2
    - meta-llama/Llama-2-7b
    - meta-llama/Llama-2-13b

  OPENAI:
    - gpt-3.5-turbo
    - gpt-4
    - gpt-4-turbo
```

### Query with Different Models

**Using Default (Local):**
```bash
python src/main.py query "What is attention?"
```

**Using Local Model:**
```bash
python src/main.py query "What is attention?" --llm google/flan-t5-base
```

**Using OpenAI Model (requires `OPENAI_API_KEY`):**
```bash
python src/main.py query "What is attention?" --llm gpt-4
```

### Programmatic LLM Switching

```python
from src.rag.pipeline import set_llm, run_rag_pipeline

# Switch to GPT-4
set_llm("gpt-4")
answer = run_rag_pipeline("Your question")

# Override at query time
answer = run_rag_pipeline("Your question", llm_model="gpt-3.5-turbo")
```

---

The system exposes a clean CLI for both **pipeline setup** and **query execution**.

### Pipeline Setup

Run the full ingestion → embedding → indexing pipeline:

```bash
python src/main.py setup
```

Skip individual stages if artifacts already exist:

```bash
# Skip PDF ingestion
python src/main.py setup --skip-ingestion

# Skip embedding generation
python src/main.py setup --skip-embedding

# Skip FAISS index building
python src/main.py setup --skip-indexing
```

This design enables **incremental rebuilds**, which mirrors real-world ML workflows.

---

### Query the RAG System

Ask questions over the indexed document corpus:

```bash
python src/main.py query "What is attention?"
```

Control retrieval depth:

```bash
python src/main.py query "Explain transformers" --top-k 5
```

The system retrieves the most relevant document chunks, formats them into a context window, and generates an answer using the configured LLM.

---

## 🧠 Design Highlights

* **Production-style CLI** using subcommands (`setup`, `query`)
* **Stage-skippable pipeline** to avoid unnecessary recomputation
* **Token-aware retrieval logic** to respect LLM context limits
* **Clear abstraction boundaries** between data, retrieval, and generation
* **Model-agnostic LLM interface** for easy backend swapping

---

## 📦 Models & Retrieval

* **Embeddings**: Sentence-transformer based dense embeddings
* **Vector Store**: FAISS for fast similarity search
* **LLMs**: Local transformer models (e.g. FLAN-T5) or API-backed models

The retrieval depth (`top-k`) can be dynamically adjusted based on estimated token usage to prevent context overflow.

---

## 🎯 Motivation

Most RAG examples exist only as notebooks. This project focuses on building a **maintainable, extensible system** that reflects how retrieval and generation pipelines are structured in production ML environments.

The goal is to demonstrate:

* Systems thinking for ML applications
* Practical constraints such as token limits and recomputation cost
* Clean interfaces between pipeline stages

---

## 🛠️ Future Work

* FastAPI service for programmatic access
* Reranking with cross-encoders
* Streaming or chunk-aware generation
* Hybrid (sparse + dense) retrieval
* Evaluation harness for retrieval quality

---

## 📄 License

MIT License
