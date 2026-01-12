from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# source_id -> { "db": FAISS, "name": str }
VECTOR_STORES = {}

def create_store(source_id: str, texts: list[str], source_name: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.from_texts(texts, embeddings)

    VECTOR_STORES[source_id] = {
        "db": db,
        "name": source_name
    }

def get_store(source_id: str):
    return VECTOR_STORES.get(source_id)
