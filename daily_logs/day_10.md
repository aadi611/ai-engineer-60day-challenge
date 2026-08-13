# Day 10 — Production RAG: Re-ranking with Cross-Encoders + DSA: Binary Search Trees

**Track A (DSA):** Binary Search Trees — problem(s) solved.
**Track B (Core build):** Built `05_reranking.py` — takes the wide candidate set from `HybridSearcher` (top_k=20) and re-scores each (query, chunk) pair with a local cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) instead of Cohere's hosted rerank endpoint, keeping the top 3. One surprising thing: on the HNSW test query, the cross-encoder pulled the correct chunk to a clear lead (score 8.1 vs. -11.2 for the rest) even though RRF had it in a near-tie with an unrelated chunk (0.0328 vs 0.0317) — a good concrete example of why bi-encoder retrieval scores alone aren't enough for precision-sensitive ranking.
**Track C (Systems):** —

**Blockers:** —
**Tomorrow:** Query transformation (HyDE, multi-query, decomposition).
