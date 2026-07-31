# Phase 1: Advanced Production RAG (Days 7-15)

## Day wise plan

- **Day 7** — Vector DB internals (HNSW, IVF, product quantization). Compare Pinecone vs Weaviate vs pgvector vs FAISS on recall/latency/cost tradeoffs.
- **Day 8** — Chunking strategies: fixed, recursive, semantic, hierarchical.
- **Day 9** — Hybrid search (BM25 + vector), reciprocal rank fusion.
- **Day 10** — Re-ranking with cross-encoders / Cohere rerank.
- **Day 11** — Query transformation: HyDE, multi-query, query decomposition.
- **Day 12** — Context compression & long-context strategies.
- **Day 13** — RAG evaluation: RAGAS, faithfulness/groundedness, LLM-as-judge.
- **Day 14** — Build & ship: end-to-end production RAG project combining everything above.
- **Day 15** — 🎯 Review + System Design #2: "Design a RAG system for 10M documents, <500ms p99."

## Resources

- [LangChain docs](https://python.langchain.com/docs/introduction/)
- [RAGAS docs](https://docs.ragas.io/)
- [Pinecone learning center](https://www.pinecone.io/learn/)

## Deliverable

A working RAG pipeline with hybrid search + re-ranking + an actual eval harness (not just vibes) reporting faithfulness/groundedness scores.
