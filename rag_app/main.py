from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.ingest import read_pdf, read_docx, read_url
from backend.store import create_store
from backend.rag import retrieve_answer, insight_lens_enrich, compare_answer
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
from dotenv import load_dotenv
import uuid
import shutil
import os
import json

# --------------------------------------------------
# ENV + APP
# --------------------------------------------------
load_dotenv()

app = FastAPI(title="Insight Lens RAG")

# --------------------------------------------------
# FRONTEND
# --------------------------------------------------
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# --------------------------------------------------
# LLM (GROQ – INSTANT)
# --------------------------------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# --------------------------------------------------
# TAVILY (WEB SEARCH)
# --------------------------------------------------
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY") or ""
)

# --------------------------------------------------
# INGEST
# --------------------------------------------------
@app.post("/upload")
async def upload(file: UploadFile):
    source_id = str(uuid.uuid4())
    temp = f"temp_{file.filename}"

    with open(temp, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if file.filename.lower().endswith(".pdf"):
        texts = read_pdf(temp)
    elif file.filename.lower().endswith(".docx"):
        texts = read_docx(temp)
    else:
        texts = []

    os.remove(temp)
    create_store(source_id, texts, file.filename)

    return {"source_id": source_id, "name": file.filename}


@app.post("/add_url")
async def add_url(url: str = Form(...)):
    source_id = str(uuid.uuid4())
    texts = read_url(url)
    create_store(source_id, texts, url)

    return {"source_id": source_id, "name": url}


# --------------------------------------------------
# NORMAL RAG (JSON STREAM)
# --------------------------------------------------
@app.post("/ask")
async def ask(
    query: str = Form(...),
    sources: str = Form(...)
):
    source_ids = [s for s in sources.split(",") if s.strip()]

    def event_stream():
        for chunk in retrieve_answer(query, source_ids, llm):
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(
        event_stream(),
        media_type="application/json"
    )


# --------------------------------------------------
# INSIGHT LENS (QUERY-LEVEL WEB ENRICHMENT)
# --------------------------------------------------
@app.post("/insight_lens")
async def insight_lens(query: str = Form(...)):
    result = insight_lens_enrich(query, llm)
    return JSONResponse(result)


# --------------------------------------------------
# TEXT + WEB INSIGHT LENS (GOOGLE LENS STYLE)
# --------------------------------------------------
@app.post("/text_web_lens")
async def text_web_lens(text: str = Form(...)):
    """
    Google-Lens–style understanding for selected text:
    - Identify concept
    - Enrich with web info
    - Return explanation + web sources
    """

    # 🔍 Web search
    search = tavily.search(
        query=text,
        search_depth="basic",
        max_results=5
    )

    sources = [
        {"title": r["title"], "url": r["url"]}
        for r in search.get("results", [])
    ]

    web_context = "\n".join(
        f"{r['title']}: {r['content']}"
        for r in search.get("results", [])
    )

    # 🧠 LLM explanation
    messages = [
        SystemMessage(
            content=(
                "You are a Web Insight Lens.\n"
                "Explain the selected text clearly and concisely.\n\n"
                "Include:\n"
                "- What it is\n"
                "- Why it matters\n"
                "- How it works\n"
                "- Key facts from web context\n"
                "Use simple language."
            )
        ),
        HumanMessage(
            content=f"""
Selected Text:
{text}

Web Information:
{web_context}
"""
        )
    ]

    answer = ""
    for chunk in llm.stream(messages):
        if chunk.content:
            answer += chunk.content

    return JSONResponse({
        "answer": answer,
        "sources": sources
    })


# --------------------------------------------------
# COMPARE MODE
# --------------------------------------------------
@app.post("/compare")
async def compare(
    query: str = Form(...),
    sources: str = Form(...)
):
    source_ids = [s for s in sources.split(",") if s.strip()]
    result = compare_answer(query, source_ids, llm)
    return JSONResponse(result)
