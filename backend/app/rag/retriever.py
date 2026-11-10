from app.rag.loader import load_documents
from app.rag.chunker import chunk
from app.rag.vector_store import build, search

_built = False

def ensure_index() -> None:
    global _built
    if _built:
        return
    docs = load_documents()
    all_chunks = []
    for d in docs:
        all_chunks.extend(chunk(d["text"]))
    build(all_chunks)
    _built = True

def retrieve(query: str, k: int = 3) -> list[str]:
    ensure_index()
    return search(query, k)
