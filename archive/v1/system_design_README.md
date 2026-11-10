# System Design Track

One System Design Day per week (marked 🎯 in [../progress_tracker.md](../progress_tracker.md)).
Each rep: 45-60 min timed design under interview conditions, then write it up
here — the write-up is what you review the night before a real interview.

## Framework to apply every time

1. **Clarify requirements** — functional + non-functional (latency, scale, cost, consistency)
2. **Back-of-envelope estimation** — QPS, data volume, storage
3. **High-level architecture** — draw it, name every component
4. **Deep dive on 2-3 components** — the interviewer's real interest
5. **Bottlenecks & tradeoffs** — where does this break, what would you change at 10x scale
6. **Monitoring & failure modes** — what pages you at 3am

## The 8 reps

| Day | Prompt |
|---|---|
| 6 | Design a low-latency LLM inference service |
| 15 | Design a RAG system for 10M documents, <500ms p99 |
| 25 | Design a multi-agent customer support platform |
| 29 | Design a ChatGPT-like product (GenAI system design framework practice) |
| 29 | Design semantic search at scale |
| 30 | Full mock #1 (timed, pick a fresh prompt) |
| 30 | Full mock #2 (timed, pick a fresh prompt) |
| 40 | Design a multi-tenant AI platform deployed on Azure |
| 48 | Design an observability/reliability layer for an LLM platform at scale |
| 52 | Design a cost-aware model-routing layer (small vs large model selection) |

(That's more than 8 — use the extras as a bank if you want additional reps or a real mock runs short.)

## Folder structure

```
system_design/
├── 01_llm_inference_service.md
├── 02_rag_10m_docs.md
├── 03_multiagent_support.md
├── 04_chatgpt_like_product.md
├── 05_semantic_search_scale.md
├── mock_01.md
├── mock_02.md
├── 06_azure_multitenant.md
├── 07_observability_layer.md
└── 08_cost_aware_routing.md
```

Each write-up: problem statement, your architecture diagram (ASCII or link to
an image), the tradeoffs you called out, and — critically — what you'd say
differently if you did it again. That last part is what actually improves
your interview performance rep over rep.

## ML-specific vs GenAI-specific framing

Classic ML system design (recommendation systems, fraud detection, ranking)
and GenAI system design (RAG, agents, LLM serving) get asked differently —
practice both framings explicitly on Day 28-29 rather than assuming one
covers the other.
