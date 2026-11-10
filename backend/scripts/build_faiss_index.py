from app.rag.retriever import ensure_index

if __name__ == "__main__":
    ensure_index()
    print("FAISS index built.")
