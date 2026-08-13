# Day 9 — Production RAG: Embeddings, Retrieval & Hybrid Search + DSA: Trees intro

**Track A (DSA):** Trees intro — problem(s) solved.
**Track B (Core build):** Built `03_embeddings_retrieval.py` — brute-force cosine-similarity vector store using a local sentence-transformers model (`all-MiniLM-L6-v2`), no API key/cost. Then built `04_hybrid_search.py` — combines BM25 (keyword) and vector search via reciprocal rank fusion (RRF), so exact-term matches (IDs, acronyms) aren't lost to purely semantic ranking. One surprising thing: RRF needs no score normalization between BM25 and cosine similarity — just rank position — which sidesteps the usual pain of combining incomparable score scales.
**Track C (Systems):** —

**Blockers:** —
**Tomorrow:** Re-ranking with cross-encoders.
