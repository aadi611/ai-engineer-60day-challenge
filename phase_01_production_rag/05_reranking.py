"""Step 5: re-rank hybrid search candidates with a cross-encoder.

Hybrid search (BM25 + vector, fused via RRF) is fast but scores each
document independently of the query -- a bi-encoder embeds query and
chunk separately and compares vectors, so it can't model fine-grained
query-chunk interactions. A cross-encoder feeds the (query, chunk) pair
into one transformer and outputs a relevance score directly, which is
far more accurate but too slow to run over an entire corpus.

The standard pattern: retrieve a wide candidate set cheaply (hybrid
search, top_k=20), then re-rank just those candidates with the
cross-encoder and keep the top few. Uses a local cross-encoder model
(no API key, no cost) instead of Cohere's hosted rerank endpoint.
"""

from importlib import import_module

from sentence_transformers import CrossEncoder

hybrid_search = import_module("04_hybrid_search")

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    """Re-scores (query, chunk) pairs with a cross-encoder."""

    def __init__(self) -> None:
        self.model = CrossEncoder(RERANK_MODEL)

    def rerank(self, query: str, candidates: list[dict], top_k: int = 3) -> list[dict]:
        pairs = [(query, c["text"]) for c in candidates]
        scores = self.model.predict(pairs)

        reranked = [
            {**c, "rerank_score": float(score)}
            for c, score in zip(candidates, scores)
        ]
        reranked.sort(key=lambda c: c["rerank_score"], reverse=True)
        return reranked[:top_k]
        
    def rerank2(self, query :str, candidates:


if __name__ == "__main__":
    chunking = import_module("02_chunking")
    documents = chunking.load_documents()
    chunks = chunking.chunk_documents(documents)
    print(f"Indexing {len(chunks)} chunks from {len(documents)} documents...\n")

    searcher = hybrid_search.HybridSearcher(chunks)
    reranker = Reranker()

    query = "HNSW approximate nearest neighbor search"

    candidates = searcher.search(query, top_k=20)
    print(f"Query: {query!r}\n")
    print(f"-- Hybrid search top {len(candidates)} candidates (before rerank) --")
    for c in candidates:
        print(f"  {c['source']} #{c['chunk_id']} (rrf_score={c['score']:.4f})")

    results = reranker.rerank(query, candidates, top_k=3)
    print(f"\n-- Cross-encoder rerank, top {len(results)} --")
    for r in results:
        print(f"--- {r['source']} #{r['chunk_id']} (rerank_score={r['rerank_score']:.4f}) ---")
        print(r["text"])
        print()
