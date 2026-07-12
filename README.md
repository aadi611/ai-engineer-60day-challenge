# 🚀 AI Engineer 60-Day Interview-Ready Challenge

A 60-day, interview-first curriculum to go from "already shipping GenAI apps" to
**production-grade AI Engineer, interview-ready**. Rebuilt from the original
RAG/Agents/Azure/Reliability/Cost structure, now with LLM internals, ML/GenAI
system design, and daily DSA practice woven in as parallel tracks instead of
being an afterthought at the end.

**Start Date:** 2026-07-12
**Target Completion:** 2026-09-09 (Day 60)
**Commitment:** ~3-4 hrs/day

---

## 🧭 How each day works (the three tracks)

Every day (except review/capstone/sprint days) is split into three blocks:

| Block | Time | What |
|---|---|---|
| **A — DSA** | ~45 min | Pattern-based coding practice (see [dsa_practice/README.md](dsa_practice/README.md)) |
| **B — Core Build** | ~2-2.5 hrs | That day's phase topic: theory + hands-on implementation |
| **C — Systems Thinking** | ~30-45 min | Reading/notes on system design, or on the weekly system-design day, a full timed design exercise |

One day per week is a **System Design Day** — Track B is replaced by a full
timed ML/GenAI system design exercise (see [system_design/README.md](system_design/README.md)).

---

## 📚 Phase Structure

### Phase 0: LLM & Transformer Foundations (Days 1-6)
Interview-grade depth on how the models you're building with actually work.
- Attention, multi-head attention, positional encoding
- Tokenization (BPE/SentencePiece), embeddings, context windows
- Pretraining objectives, scaling laws, model family differences (GPT/Llama/Claude/Gemini)
- Fine-tuning: full FT, LoRA/QLoRA, PEFT, instruction tuning
- Alignment: RLHF, DPO, RLAIF, guardrails
- Inference optimization: KV cache, quantization (GPTQ/AWQ), speculative decoding, batching

### Phase 1: Advanced Production RAG (Days 7-15)
- Vector DB internals (HNSW, IVF, PQ) — Pinecone vs Weaviate vs pgvector vs FAISS
- Chunking strategies, hybrid search (BM25 + vector, RRF)
- Re-ranking, query transformation (HyDE, multi-query, decomposition)
- Context compression, long-context strategies
- RAG evaluation (RAGAS, faithfulness/groundedness, LLM-as-judge)
- **Ship:** production RAG project

### Phase 2: Agentic Systems & Orchestration (Days 16-25)
- ReAct, tool/function calling, LangGraph fundamentals
- Multi-agent patterns (supervisor, swarm, hierarchical), agent memory
- Human-in-the-loop, agent observability (LangSmith/tracing)
- MCP & tool ecosystems, prompt-injection defense/guardrails
- **Ship:** multi-agent project

### Phase 3: ML/DL & System Design Deep Dive (Days 26-30)
- Classic ML interview fundamentals (bias-variance, regularization, ensembles, metrics)
- DL fundamentals refresher (backprop, CNN/RNN, optimizers, normalization)
- ML system design framework + GenAI system design framework
- Two full timed mock system-design interviews

### Phase 4: Azure Deployment & Productionization (Days 31-40)
- Azure OpenAI Service, Azure AI Search, Managed Identity/Key Vault
- Docker best practices, Container Apps/AKS, API Management
- CI/CD (GitHub Actions), blue-green/canary deployments, security
- **Ship:** deploy RAG+agent app end-to-end on Azure

### Phase 5: Reliability, Scaling & Observability (Days 41-48)
- Rate limiting/throttling, retries/circuit breakers, graceful degradation
- Load testing (locust/k6), caching (semantic cache, Redis)
- Async processing/queues, distributed tracing, OpenTelemetry/Prometheus
- **Ship:** reliability layer on capstone

### Phase 6: Cost Optimization (Days 49-52)
- Token optimization/prompt compression, model routing (small vs large)
- Cost monitoring/alerting (FinOps for AI), batch processing optimization

### Phase 7: Capstone — Enterprise Copilot (Days 53-57)
Architecture → core build → integration (agents + RAG + reliability + cost) → testing/docs → polish for portfolio.

### Phase 8: Interview Sprint (Days 58-60)
Resume/portfolio polish, full mock interview loop (technical + system design + behavioral), gap-fill on weak spots.

---

## 🛠️ Tech Stack

- **AI/ML:** OpenAI, Anthropic, LangChain, LangGraph, HuggingFace
- **Cloud:** Azure (OpenAI, AI Search, Container Apps, AKS, API Management)
- **Vector/Search:** ChromaDB, FAISS, Pinecone, pgvector, BM25
- **Backend:** FastAPI, Python 3.11+
- **Observability:** Prometheus, OpenTelemetry, LangSmith
- **Load testing:** locust, k6
- **Containerization:** Docker, Docker Compose

## Prerequisites

- Python 3.12+, Docker & Docker Compose
- OpenAI and/or Anthropic API key
- Azure subscription (for Phase 4+)
- A LeetCode (or similar) account for DSA tracking

## 📁 Project Structure

```
ai-engineer-60day-challenge/
├── phase_00_llm_foundations/
├── phase_01_production_rag/
├── phase_02_agentic_orchestration/
├── phase_03_system_design_ml/
├── phase_04_azure_deployment/
├── phase_05_reliability_scaling/
├── phase_06_cost_optimization/
├── phase_07_capstone_copilot/
├── phase_08_interview_sprint/
├── dsa_practice/            # daily coding problems by pattern
├── system_design/           # weekly design write-ups + mocks
├── shared_utils/
├── datasets/
├── daily_logs/
└── progress_tracker.md
```

## 📊 Progress Tracking

Day-by-day checklist lives in [progress_tracker.md](progress_tracker.md).

## 🎯 Goals

- ✅ Explain transformer internals and inference optimization at interview depth
- ✅ Ship a production RAG system with real evaluation
- ✅ Ship a multi-agent orchestration system
- ✅ Pass ML/GenAI system design interviews (practiced 8x)
- ✅ Deploy and productionize on Azure with reliability + cost controls
- ✅ Clear 90+ DSA problems across core interview patterns
- ✅ Ship an enterprise copilot capstone for the portfolio
- ✅ Be mock-interview tested across technical, system design, and behavioral

---

**Current Phase:** Phase 0
