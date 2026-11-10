from pathlib import Path

KB_DIR = Path(__file__).resolve().parents[2] / "knowledge_base"

def load_documents() -> list[dict]:
    docs = []
    for p in KB_DIR.glob("*.md"):
        docs.append({"source": p.name, "text": p.read_text(encoding="utf-8")})
    return docs
