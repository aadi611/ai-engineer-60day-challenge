"""Step 3: embed chunks, store them, and retrieve by cosine similarity.

Builds on 02_chunking.py. No LLM generation yet -- just indexing +
retrieval, so you can inspect which chunks a query actually pulls back
before wiring in the final answer-generation step
Uses a local sentence-transformers model for embeddings (no API key,
no cost) instead of the OpenAI embeddings API.
"""

from importlib import import_module

import numpy as np
from sentence_transformers import SentenceTransformer

chunking = import_module("02_chunking")

EMBED_MODEL = "all-MiniLM-L6-v2"

class VectorStore:
    """Minimal in-memory vector store: brute-force cosine similarity search."""
    def __init__(self) -> None:
        self.model = SentenceTransformer(EMBED_MODEL)
        self.chunks: list[dict] = []
        self.vectors: np.ndarray | None = None

    def add(self, chunks: list[dict]) -> None:
        embeddings = self.model.encode(
            [c["text"] for c in chunks], convert_to_numpy=True, normalize_embeddings=True
        )
        self.chunks.extend(chunks)
        self.vectors = embeddings if self.vectors is None else np.vstack([self.vectors, embeddings])

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        scores = self.vectors @ query_vec
        top_indices = np.argsort(-scores)[:top_k]
        return [
            {**self.chunks[i], "score": float(scores[i])}
            for i in top_indices
        ]


if __name__ == "__main__":
    documents = chunking.load_documents()
    chunks = chunking.chunk_documents(documents)
    print(f"Indexing {len(chunks)} chunks from {len(documents)} documents...\n")

    store = VectorStore()
    store.add(chunks)

    query = "How does a vector database help with retrieval?"
    results = store.search(query, top_k=3)

    print(f"Query: {query!r}\n")
    for r in results:
        print(f"--- {r['source']} #{r['chunk_id']} (score={r['score']:.4f}) ---")
        print(r["text"])
        print()
