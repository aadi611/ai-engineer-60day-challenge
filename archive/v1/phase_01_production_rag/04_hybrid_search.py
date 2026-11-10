"""Step 4: hybrid search -- combine BM25 (keyword) and vector search
using reciprocal rank fusion (RRF).

Vector search is great at semantic similarity but can miss exact terms
(IDs, acronyms, rare words). BM25 is great at exact terms but misses
paraphrases. RRF merges both rankings without needing to normalize or
compare their raw scores directly.
"""

from importlib import import_module

import numpy as np
from rank_bm25 import BM25Okapi

chunking = import_module("02_chunking")
embeddings_retrieval = import_module("03_embeddings_retrieval")


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


class HybridSearcher:
    """Combines a BM25 index and a VectorStore over the same chunks via RRF."""

    def __init__(self, chunks: list[dict]) -> None:
        self.chunks = chunks
        self.bm25 = BM25Okapi([_tokenize(c["text"]) for c in chunks])
        self.vector_store = embeddings_retrieval.VectorStore()
        self.vector_store.add(chunks)

    def _bm25_ranking(self, query: str) -> list[int]:
        scores = self.bm25.get_scores(_tokenize(query))
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    def _vector_ranking(self, query: str) -> list[int]:
        query_vec = self.vector_store.model.encode(
            [query], convert_to_numpy=True, normalize_embeddings=True
        )[0]
        scores = self.vector_store.vectors @ query_vec
        return list(np.argsort(-scores))

    def search(self, query: str, top_k: int = 3, rrf_k: int = 60) -> list[dict]:
        """Rank by 1/(rrf_k + rank) summed across the BM25 and vector rankings."""
        bm25_order = self._bm25_ranking(query)
        vector_order = self._vector_ranking(query)

        fused_scores: dict[int, float] = {}
        for rank, idx in enumerate(bm25_order):
            fused_scores[idx] = fused_scores.get(idx, 0.0) + 1.0 / (rrf_k + rank + 1)
        for rank, idx in enumerate(vector_order):
            fused_scores[idx] = fused_scores.get(idx, 0.0) + 1.0 / (rrf_k + rank + 1)

        top_indices = sorted(fused_scores, key=lambda i: fused_scores[i], reverse=True)[:top_k]
        return [{**self.chunks[i], "score": fused_scores[i]} for i in top_indices]


if __name__ == "__main__":
    documents = chunking.load_documents()
    chunks = chunking.chunk_documents(documents)
    print(f"Indexing {len(chunks)} chunks from {len(documents)} documents...\n")

    searcher = HybridSearcher(chunks)

    query = "HNSW approximate nearest neighbor search"
    results = searcher.search(query, top_k=3)

    print(f"Query: {query!r}\n")
    for r in results:
        print(f"--- {r['source']} #{r['chunk_id']} (rrf_score={r['score']:.4f}) ---")
        print(r["text"])
        print()
