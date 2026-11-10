# Phase 2: Secure Production RAG (Days 17-25)

v1 RAG plus the two things most RAG tutorials skip: **who is allowed to see which chunk**, and
**what happens when a document is hostile**.

> **v1 reference:** [../archive/v1/phase_01_production_rag/](../archive/v1/phase_01_production_rag/) has your
> chunking, embeddings, hybrid search (RRF) and cross-encoder reranking scripts plus sample data. Rebuild
> them as a package this time (`rag/chunking.py`, `rag/retrieve.py`, ...) instead of numbered scripts with
> `import_module`. Note that v1 `05_reranking.py` has broken imports (`from time import datetime`, `import logger`).

## Days

- **Day 17: Vector index internals.** Flat, HNSW, IVF, product quantization; recall/latency/memory tradeoffs;
  pgvector vs Qdrant vs FAISS vs managed (Pinecone, Azure AI Search).
- **Day 18: Parsing & chunking.** PDFs/tables/HTML parsing; fixed, recursive, semantic, hierarchical chunking;
  [contextual retrieval](https://www.anthropic.com/news/contextual-retrieval) (prepend chunk context before embedding).
- **Day 19: Hybrid search.** BM25 + dense vectors, reciprocal rank fusion, and when keyword search wins (IDs, CVE numbers, error codes).
- **Day 20: Re-ranking + query transformation.** Cross-encoders / rerank APIs; HyDE, multi-query, decomposition.
- **Day 21: Beyond basic RAG.** Agentic RAG (retrieval as a tool), GraphRAG, long-context vs RAG, context compression.
- **Day 22: 🔐 Permission-aware RAG.** Document-level ACLs carried into chunk metadata, **filter at query time
  (never post-filter in the prompt)**, tenant isolation (separate indexes vs namespaces vs row-level security
  in pgvector), PII detection/redaction with [Presidio](https://microsoft.github.io/presidio/), data residency.
- **Day 23: 🔐 RAG attacks & defenses.** Indirect prompt injection inside documents, knowledge-base poisoning
  (PoisonedRAG-style), data exfiltration via rendered markdown images/links, embedding inversion, retrieval DoS.
  Defenses: content provenance, trust tiers, spotlighting/delimiting, output link allow-lists, retrieval monitoring.
- **Day 24: RAG evaluation.** Golden question sets, [RAGAS](https://docs.ragas.io/) (faithfulness, context
  precision/recall), LLM-as-judge calibration against human labels, eval-driven development.
- **Day 25: 🎯 Ship + SD #3.** Secure RAG service behind your Phase 1 gateway: hybrid + rerank, ACL filtering,
  PII redaction, eval harness **and** an injection test suite (poisoned docs that must not change behaviour).
  **SD #3:** *RAG for 10M documents, <500 ms p99, with per-user permissions.*

## Deliverables

- `rag/` package + `evals/` (quality) + `attacks/` (poisoned-document suite) with a results table in the README
- SD #3 write-up
