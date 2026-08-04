"""Step 3: embed chunks, store them, and retrieve by cosine similarity.

Builds on 02_chunking.py. No LLM generation yet -- just indexing +
retrieval, so you can inspect which chunks a query actually pulls back
before wiring in the final answer-generation step.
"""

import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from importlib import import_module

chunking = import_module("02_chunking")

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = "text-embedding-3-small"


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a batch of texts, returning an (n, dim) float32 array."""
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype=np.float32)


class VectorStore:
    """Minimal in-memory vector store: brute-force cosine similarity search."""

    def __init__(self) -> None:
        self.chunks: list[dict] = []
        self.vectors: np.ndarray | None = None

    def add(self, chunks: list[dict]) -> None:
        embeddings = embed_texts([c["text"] for c in chunks])
        normed = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.chunks.extend(chunks)
        self.vectors = normed if self.vectors is None else np.vstack([self.vectors, normed])

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_vec = embed_texts([query])[0]
        query_vec = query_vec / np.linalg.norm(query_vec)
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
