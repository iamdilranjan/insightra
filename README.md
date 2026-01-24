<p align="center">
  <img src="https://github.com/user-attachments/assets/d0b05b81-d168-498c-ae67-87c46e638817" width="800" />
</p>

<h1 align="center">🚀 Insightra</h1>

<p align="center">
  <b>From Data to Decisions.</b><br>
  AI-powered RAG backend to upload PDFs, scan URLs, ingest raw text, and retrieve intelligent, context-aware insights.
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-Backend-success" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10+-blue" /></a>
  <a href="#"><img src="https://img.shields.io/badge/LLM-Groq-purple" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Search-Tavily-orange" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Framework-LangChain-red" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Deploy-Render-black" /></a>
</p>

---

## 🌟 Why Insightra?

Modern information is scattered across documents, web pages, and raw text. **Insightra** unifies all of this into a single intelligent search and insight engine powered by RAG (Retrieval-Augmented Generation) architecture.

With Insightra, you can:
- 📄 Upload and process documents  
- 🌐 Crawl and extract web content  
- 🧠 Build searchable knowledge bases  
- 🔍 Query using natural language  
- 📚 Get AI-powered, source-backed answers  

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📄 PDF Ingestion | Upload and parse PDF documents |
| 🌐 URL Crawling | Extract structured content from webpages |
| 🧠 RAG Architecture | Retrieval-Augmented Generation using LangChain |
| 🔍 Semantic Search | Vector-based similarity matching |
| 📚 Source Citations | Transparent answer sourcing |
| ⚡ FastAPI Backend | High-performance async APIs |
| 🔐 Secure Configuration | Environment-based API keys |
| ☁️ Cloud Ready | Deploy on Render, Railway, or AWS |
| 🧩 Modular Design | Easy to extend and customize |

---

## 🧠 How It Works

1. **Ingest** – Upload PDFs, URLs, or raw text via API  
2. **Process** – Extract, chunk, and clean content using LangChain text splitters  
3. **Embed** – Generate vector embeddings for semantic search  
4. **Store** – Save in vector database with metadata  
5. **Retrieve** – Semantic + keyword search across stored knowledge  
6. **Generate** – LLM synthesizes context-aware answers using retrieved chunks  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| ⚙️ Backend | FastAPI |
| 🧠 LLM | Groq (llama-3.1-70b) |
| 🔗 Framework | LangChain |
| 🌐 Web Search | Tavily API |
| 🗄️ Vector Store | Chroma / FAISS |
| 📊 Embeddings | Sentence Transformers |
| 🐍 Language | Python 3.10+ |
| ☁️ Deployment | Render |

---

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.10
pip
virtualenv (recommended)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/insightra.git
cd insightra

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

---



### 4. Health Check
```bash
GET /health
```

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM | Yes |
| `TAVILY_API_KEY` | API key for Tavily search | Yes |
| `VECTOR_DB_PATH` | Path to vector database | No (default: ./db) |
| `MAX_FILE_SIZE` | Max upload size in MB | No (default: 10) |

---
