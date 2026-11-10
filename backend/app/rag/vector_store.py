"""Deterministic keyword retriever for the local policy knowledge base."""
import re

_docs: list[str] = []


def build(chunks: list[str]) -> None:
    global _docs
    _docs = chunks


def search(query: str, k: int = 3) -> list[str]:
    query_terms = {
        term for term in re.findall(r"[a-z0-9_]+", query.lower()) if len(term) > 2
    }
    if not query_terms:
        return []

    ranked = []
    for document in _docs:
        document_terms = set(re.findall(r"[a-z0-9_]+", document.lower()))
        score = len(query_terms & document_terms)
        if score:
            ranked.append((score, document))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in ranked[:k]]
