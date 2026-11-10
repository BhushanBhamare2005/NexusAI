"""Lazy-loaded sentence-transformer embedder."""
_model = None

def embed(texts: list[str]) -> list[list[float]]:
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model.encode(texts, convert_to_numpy=False, normalize_embeddings=True).tolist()
