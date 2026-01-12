🚀 Insightra

Insightra is an AI-powered backend platform that enables users to upload PDFs, scan URLs, ingest raw text, and retrieve intelligent, context-aware insights from both private documents and the open web.

From Data to Decisions.
![WhatsApp Image 2026-01-12 at 23 56 31](https://github.com/user-attachments/assets/d0b05b81-d168-498c-ae67-87c46e638817)

🌟 Why Insightra?

Modern information is scattered across documents, web pages, and raw text. Insightra unifies all of this into a single intelligent search and insight engine.

With Insightra, you can:

Upload documents

Crawl URLs

Extract and store knowledge

Query using natural language

Get AI-powered, source-backed answers

✨ Core Features

📄 PDF ingestion & processing

🌐 URL scanning & crawling

🧠 AI-powered semantic search

🔍 Context-aware retrieval

📚 Source-based answers

⚡ High-performance FastAPI backend

🔐 Secure API key handling

☁️ Cloud deployment ready (Render)

🧩 Modular architecture

🧠 How It Works

Ingest – Upload PDFs, URLs, or raw text

Process – Extract, chunk, clean, and embed

Store – Save in vector + metadata stores

Search – Semantic + keyword + web fusion

Answer – AI generates contextual responses

🏗️ Tech Stack
Layer	Technology
Backend	FastAPI
LLM	Groq
Web Search	Tavily
Vector Store	(Your current one)
Language	Python 3.10+
Deployment	Render
📁 Project Structure
insightra-backend/
│
├── main.py
├── requirements.txt
│
├── backend/
│   ├── rag/
│   ├── ingest/
│   ├── store/
│   ├── verifier/
│   └── utils/
│
├── frontend/
│   └── index.html
│
├── .env.example
├── .gitignore
└── README.md

🔐 Environment Variables

Create a .env file (never commit this):

GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

⚙️ Local Development
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/insightra-backend.git
cd insightra-backend

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Server
uvicorn main:app --reload


Visit:

http://localhost:8000
