from backend.store import get_store
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os

# ---------------- TAVILY CLIENT ----------------
# (Best practice: move key to .env later)
tavily = TavilyClient(
    api_key="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"
)

# =====================================================
# 🔹 LLM-BASED FOLLOW-UP QUESTION GENERATOR
# =====================================================
def generate_followups(query: str, answer: str, llm):
    """
    Uses LLM to generate intelligent, context-aware follow-up questions
    based on user intent and the generated answer.
    """

    messages = [
        SystemMessage(
            content=(
                "You are an AI research assistant.\n"
                "Based on the user's question and the answer, "
                "generate 3 to 4 smart follow-up questions.\n\n"
                "Rules:\n"
                "- Questions must help the user explore deeper\n"
                "- Do NOT repeat the original question\n"
                "- Keep questions short and clear\n"
                "- Do NOT add explanations\n"
                "- Return ONLY a numbered list"
            )
        ),
        HumanMessage(
            content=f"""
User Question:
{query}

Answer:
{answer}
"""
        )
    ]

    response = llm.invoke(messages).content

    followups = []
    for line in response.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            followups.append(line.split(".", 1)[1].strip())

    return followups[:4]


# =====================================================
# 🔹 DOCUMENT RAG (STREAMING + FOLLOW-UPS)
# =====================================================
def retrieve_answer(query: str, source_ids: list[str], llm):
    docs = []

    # 🔍 Retrieve from selected sources
    for sid in source_ids:
        store = get_store(sid)
        if not store:
            continue

        results = store["db"].similarity_search(query, k=3)
        docs.extend(results)

    if not docs:
        yield {
            "type": "answer",
            "content": "No relevant information found in selected sources."
        }
        return

    context = "\n".join(d.page_content for d in docs)

    messages = [
        SystemMessage(
            content="Answer strictly from the provided context."
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{query}"
        )
    ]

    full_answer = ""

    # 🔄 Stream answer tokens
    for chunk in llm.stream(messages):
        if chunk.content:
            full_answer += chunk.content
            yield {
                "type": "answer",
                "content": chunk.content
            }

    # 🧠 Generate LLM-based follow-up questions
    followups = generate_followups(query, full_answer, llm)

    yield {
        "type": "followups",
        "content": followups
    }


# =====================================================
# 🔹 INSIGHT LENS (WEB ENRICHMENT USING TAVILY)
# =====================================================
def insight_lens_enrich(query: str, llm):
    search = tavily.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    sources = [
        {"title": r["title"], "url": r["url"]}
        for r in search["results"]
    ]

    web_context = "\n".join(
        f"{r['title']}: {r['content']}"
        for r in search["results"]
    )

    messages = [
        SystemMessage(
            content="You are a research assistant. Enrich the answer using web information."
        ),
        HumanMessage(
            content=f"Web Information:\n{web_context}\n\nQuestion:\n{query}"
        )
    ]

    answer = ""
    for chunk in llm.stream(messages):
        if chunk.content:
            answer += chunk.content

    return {
        "answer": answer,
        "sources": sources
    }


# =====================================================
# 🔹 COMPARE MODE (SIDE-BY-SIDE ANSWERS)
# =====================================================
def compare_answer(query: str, source_ids: list[str], llm):
    results = {}

    for sid in source_ids:
        store = get_store(sid)
        if not store:
            continue

        docs = store["db"].similarity_search(query, k=4)
        context = "\n".join(d.page_content for d in docs)

        messages = [
            SystemMessage(
                content="Answer strictly from the provided context."
            ),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion:\n{query}"
            )
        ]

        answer = ""
        for chunk in llm.stream(messages):
            if chunk.content:
                answer += chunk.content

        results[store["name"]] = answer

    return results
