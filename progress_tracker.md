# 📈 AI Engineer Challenge v2: Progress Tracker

**Start Date:** November 11, 2026
**Target Completion Date:** January 29, 2027
**Current Day:** 0 of 80 (v2 not yet started; v1 tracker is in [archive/v1/progress_tracker.md](archive/v1/progress_tracker.md))

Each day: **A** = Skills rep (odd day = DSA · even day = 🔐 security lab) · **B** = Core build (~2-2.5 hrs) · **C** = Systems & security lens (~30-45 min; full design rep on 🎯 days)

Rule: if you miss a day, **don't** skip forward. Slide the dates and use a 🛟 buffer day.

---

## Overall Progress

- [ ] **Phase 0:** Foundations: Python, LLM APIs & Internals (Days 1-8)
- [ ] **Phase 1:** Security Foundations for AI Engineers (Days 9-16)
- [ ] **Phase 2:** Secure Production RAG (Days 17-25)
- [ ] **Phase 3:** Agents, Context Engineering & Protocols (Days 26-37)
- [ ] 🛟 **Day 38:** Buffer + midpoint retro
- [ ] **Phase 4:** AI Security: Attack & Defend (Days 39-50)
- [ ] **Phase 5:** Agent Marketplaces & Agentic Commerce (Days 51-60)
- [ ] **Phase 6:** Production Platform: Deploy, Reliability, Cost (Days 61-68)
- [ ] **Phase 7:** ML Fundamentals & System Design (Days 69-71)
- [ ] **Phase 8:** Capstone: Secure Agent Marketplace (Days 72-76)
- [ ] 🛟 **Day 77:** Buffer
- [ ] **Phase 9:** Interview Sprint (Days 78-80)

---

## 📅 Phase 0: Foundations: Python, LLM APIs & Internals (Days 1-8)

- [ ] **Day 1:** Modern Python toolchain (uv, typing, Pydantic v2, async/httpx) + first Claude & OpenAI API calls (messages, streaming) + secrets hygiene (.env, gitleaks pre-commit). A: DSA, Arrays & Strings
- [ ] **Day 2:** Tokenization: build BPE from scratch; embeddings and what they encode. A: 🔐 Lab, Burp Suite setup + PortSwigger HTTP basics
- [ ] **Day 3:** Attention from scratch: scaled dot-product, multi-head, causal mask, positional encodings (sinusoidal → RoPE). A: DSA, Two Pointers
- [ ] **Day 4:** Pretraining, scaling laws, architecture variants (dense vs MoE, MHA/GQA/MQA, long-context tricks, multimodal). A: 🔐 Lab, OverTheWire Bandit 0-10
- [ ] **Day 5:** Post-training: SFT, LoRA/QLoRA, RLHF, DPO, Constitutional AI/RLAIF, **RLVR & GRPO**. Run a tiny LoRA. A: DSA, Sliding Window
- [ ] **Day 6:** Reasoning models & test-time compute: extended thinking, budgets, when to pick reasoning vs fast models. A: 🔐 Lab, Bandit 11-20
- [ ] **Day 7:** Structured outputs, tool-calling basics, prompt caching, batch APIs, context windows: prompt engineering → context engineering. A: DSA, HashMaps
- [ ] **Day 8:** 🎯 Inference optimization (KV cache, PagedAttention/vLLM, quantization, speculative decoding, continuous batching) + **SD #1:** low-latency LLM inference service. A: 🔐 Lab, Gandalf 1-4

**Phase 0 Completion:** 0% (0/8 days)

---

## 📅 Phase 1: Security Foundations for AI Engineers (Days 9-16)

- [ ] **Day 9:** Security mindset: CIA, attack surface, trust boundaries, **STRIDE threat modeling**. Threat-model a simple chatbot. A: DSA, Stacks & Queues
- [ ] **Day 10:** Web & API security: OWASP Top 10 (2025) + OWASP API Security Top 10 (injection, broken access control, SSRF, BOLA/IDOR). A: 🔐 Lab, PortSwigger SQL injection
- [ ] **Day 11:** AuthN/AuthZ: OAuth 2.1, OIDC, JWT pitfalls, API keys, RBAC/ABAC/ReBAC, least privilege. Build FastAPI + JWT auth. A: DSA, Binary Search
- [ ] **Day 12:** Applied crypto for engineers: hashing, HMAC, AEAD, public-key, TLS, digital signatures, secrets management. A: 🔐 Lab, PortSwigger JWT attacks
- [ ] **Day 13:** Networking & cloud security: DNS/HTTP/TLS, SSRF → metadata endpoints, IAM, private endpoints, zero trust. A: DSA, Linked Lists
- [ ] **Day 14:** Secure SDLC & supply chain: SAST/DAST (Semgrep, Bandit), dependency & secret scanning, SBOM, SLSA, **slopsquatting**. A: 🔐 Lab, PortSwigger SSRF
- [ ] **Day 15:** Detection & response: structured audit logs, SIEM basics, incident response, MITRE ATT&CK (bridge to ATLAS). A: DSA, Trees
- [ ] **Day 16:** 🎯 Ship: **secure LLM API gateway skeleton** (auth, rate limit, input validation, audit log, secret mgmt, scanners in pre-commit) + **SD #2:** secure multi-tenant LLM API gateway. A: 🔐 Lab, PortSwigger access control / IDOR

**Phase 1 Completion:** 0% (0/8 days)

---

## 📅 Phase 2: Secure Production RAG (Days 17-25)

- [ ] **Day 17:** Embeddings & vector index internals (flat, HNSW, IVF, PQ); pgvector vs Qdrant vs FAISS. A: DSA, Trees / BST
- [ ] **Day 18:** Document parsing + chunking (fixed, recursive, semantic, hierarchical) + **contextual retrieval**. A: 🔐 Lab, OWASP Juice Shop (part 1)
- [ ] **Day 19:** Hybrid search: BM25 + vectors, reciprocal rank fusion. A: DSA, Heaps
- [ ] **Day 20:** Re-ranking (cross-encoders) + query transformation (HyDE, multi-query, decomposition). A: 🔐 Lab, PortSwigger Web LLM attacks (1)
- [ ] **Day 21:** Agentic RAG, GraphRAG, long context vs RAG, context compression. A: DSA, Graphs (BFS/DFS)
- [ ] **Day 22:** **Permission-aware RAG:** document-level ACLs, tenant isolation, metadata filtering, PII redaction (Presidio). A: 🔐 Lab, PortSwigger Web LLM attacks (indirect injection)
- [ ] **Day 23:** **RAG attacks:** indirect prompt injection in documents, knowledge-base poisoning, markdown-image exfiltration, embedding inversion, and defenses. A: DSA, Graphs (topological sort)
- [ ] **Day 24:** RAG evaluation: golden sets, RAGAS, faithfulness, LLM-as-judge calibration, eval-driven development. A: 🔐 Lab, Gandalf 5-8
- [ ] **Day 25:** 🎯 Ship: **secure RAG** (ACLs + eval harness + injection test suite) + **SD #3:** RAG for 10M docs, <500 ms p99, per-user permissions. A: DSA, Backtracking

**Phase 2 Completion:** 0% (0/9 days)

---

## 📅 Phase 3: Agents, Context Engineering & Protocols (Days 26-37)

- [ ] **Day 26:** Agent loop **from scratch** (no framework): tool calling, ReAct, stop conditions; workflows vs agents. A: 🔐 Lab, Juice Shop (part 2)
- [ ] **Day 27:** Context engineering: tool design (agent-computer interface), just-in-time retrieval, compaction, note-taking, sub-agents. A: DSA, DP (1D)
- [ ] **Day 28:** Agent SDKs side by side: Claude Agent SDK vs OpenAI Agents SDK vs LangGraph (same agent, 3 ways). A: 🔐 Lab, Dreadnode Crucible (intro challenges)
- [ ] **Day 29:** LangGraph deep dive: state, checkpoints, interrupts (HITL), durable execution. A: DSA, DP (2D)
- [ ] **Day 30:** Multi-agent patterns: orchestrator-workers, supervisor, handoffs, and when **not** to go multi-agent. A: 🔐 Lab, Crucible (prompt injection)
- [ ] **Day 31:** Agent memory: short/long-term, episodic/semantic, memory tools, plus **memory poisoning**. A: DSA, Greedy
- [ ] **Day 32:** **MCP I:** build an MCP server (tools, resources, prompts), transports, clients, and wire it into an agent. A: 🔐 Lab, Damn Vulnerable MCP Server (1)
- [ ] **Day 33:** **MCP II:** authorization (OAuth 2.1, protected resource metadata), elicitation, structured output, MCP Registry, **Agent Skills**. A: DSA, Intervals
- [ ] **Day 34:** **A2A:** agent cards, tasks, streaming; MCP vs A2A; expose your agent over A2A. A: 🔐 Lab, Damn Vulnerable MCP Server (2)
- [ ] **Day 35:** Computer-use / browser agents + code-execution agents (intro to sandboxing). A: DSA, Union-Find
- [ ] **Day 36:** Agent evals & observability: trajectory evals, tool-call accuracy, OpenTelemetry GenAI conventions, Langfuse/LangSmith. A: 🔐 Lab, TryHackMe AI/LLM room
- [ ] **Day 37:** 🎯 Ship: **multi-agent system** (MCP tools + A2A interface + HITL + traces + evals) + **SD #4:** multi-agent customer-support platform. A: DSA, Tries

**Phase 3 Completion:** 0% (0/12 days)

- [ ] 🛟 **Day 38:** Buffer: finish anything behind, then a midpoint retro (top 3 weak areas → fold into Track A/C for the rest of the plan)

---

## 📅 Phase 4: AI Security: Attack & Defend (Days 39-50)

- [ ] **Day 39:** AI threat landscape: OWASP LLM Top 10 (2025), **OWASP Agentic Top 10 (2026)**, **OWASP MCP Top 10**, MITRE ATLAS, CSA MAESTRO. Threat-model your Phase 3 agent. A: DSA, Sliding Window (advanced)
- [ ] **Day 40:** Prompt injection & jailbreaks deep dive: direct/indirect, many-shot, encoding, multi-turn (Crescendo), **the lethal trifecta**. A: 🔐 Lab, Crucible (jailbreak set)
- [ ] **Day 41:** Injection-resistant **design**: Dual-LLM, **CaMeL**, plan-then-execute, action-selector, context minimization, spotlighting. A: DSA, mixed review
- [ ] **Day 42:** Guardrails & classifiers: Llama Guard / Prompt Guard, NeMo Guardrails, output filtering; measure false-positive and false-negative rates. A: 🔐 Lab, PortSwigger Web LLM attacks (all remaining)
- [ ] **Day 43:** Agent & tool security: excessive agency, confused deputy, least-privilege tools, HITL for high-risk actions, egress control, **sandboxing** (containers, gVisor, Firecracker microVMs). A: DSA, mixed review
- [ ] **Day 44:** **MCP security:** tool poisoning, rug pulls, tool shadowing, cross-server exfiltration, token passthrough, session hijack, OAuth/SSRF pitfalls; scan MCP servers. A: 🔐 Lab, Damn Vulnerable MCP Server (all)
- [ ] **Day 45:** Automated red teaming: **garak, PyRIT, promptfoo**; attack suite in CI. A: DSA, mixed review
- [ ] **Day 46:** Model & data supply chain: pickle exploits vs safetensors, model signing, backdoors/sleeper agents, data poisoning, AIBOM. A: 🔐 Lab, HuggingFace model-scanning exercise
- [ ] **Day 47:** Privacy attacks: membership inference, training-data extraction, model extraction/distillation, system-prompt leakage; DP basics. A: DSA, mixed review
- [ ] **Day 48:** Governance & compliance: NIST AI RMF + AI 600-1, EU AI Act, ISO/IEC 42001, SOC 2 for AI products, AI incident response. A: 🔐 Lab, write a mini AI incident post-mortem
- [ ] **Day 49:** AI **for** security: SOC-triage agent, log-analysis RAG, vuln-finding agents (AIxCC lessons). A: DSA, mixed review
- [ ] **Day 50:** 🎯 Ship: **red-team report + hardened agent v2** (before/after attack success rate) + **SD #5:** enterprise AI firewall / guardrail service. A: 🔐 Lab, CTF of your choice

**Phase 4 Completion:** 0% (0/12 days)

---

## 📅 Phase 5: Agent Marketplaces & Agentic Commerce (Days 51-60)

- [ ] **Day 51:** Marketplace landscape: MCP Registry + sub-registries, ChatGPT apps, Claude plugins/Skills marketplaces, AWS Marketplace AI agents, Microsoft/Salesforce/Google agent stores, and their business models. A: DSA, mixed review
- [ ] **Day 52:** Packaging & listing: manifests (`server.json`, agent card, plugin manifest), versioning/semver for tools, capability & permission declarations; publish to a test registry. A: 🔐 Lab, OAuth misconfiguration lab
- [ ] **Day 53:** Discovery & ranking: semantic search over capabilities (reuse your RAG), tool search, quality/reputation signals, eval-based ranking, anti-spam. A: DSA, mixed review
- [ ] **Day 54:** **Agent identity & trust:** workload identity (SPIFFE), OAuth client credentials, signed manifests, Web Bot Auth / signed agents, "Know Your Agent", verifiable credentials. A: 🔐 Lab, JWT/signature verification bugs
- [ ] **Day 55:** **Delegated authorization:** OAuth token exchange (RFC 8693), on-behalf-of, scoped short-lived tokens, consent UX, revocation; tenant isolation. A: DSA, mixed review
- [ ] **Day 56:** **Agent payments:** AP2 (mandates), ACP (agent checkout), UCP, x402 (HTTP 402), card-network agent programs; fraud & liability. **Test mode only.** A: 🔐 Lab, business-logic flaws (PortSwigger)
- [ ] **Day 57:** Metering, billing & economics: usage events, pricing models, quotas, revenue share, per-call cost attribution (Stripe test mode). A: DSA, mixed review
- [ ] **Day 58:** **Marketplace trust & safety pipeline:** automated vetting (static scan, sandboxed dynamic run, permission review, injection suite), version pinning/hashes vs rug pulls, monitoring, takedown. A: 🔐 Lab, review a real open-source MCP server
- [ ] **Day 59:** Cross-vendor interop: A2A between marketplace agents, SLAs/contracts, evals as certification, cross-org observability. A: DSA, mixed review
- [ ] **Day 60:** 🎯 Ship: **mini agent marketplace v0** (registry API + search + vetting pipeline + metered calls) + **SD #6:** agent marketplace for 10k agents / 1M users. A: 🔐 Lab, threat-model your own marketplace

**Phase 5 Completion:** 0% (0/10 days)

---

## 📅 Phase 6: Production Platform: Deploy, Reliability, Cost (Days 61-68)

- [ ] **Day 61:** Docker for AI apps: multi-stage, non-root, minimal images, image scanning (Trivy). A: DSA, mixed review
- [ ] **Day 62:** Azure: Microsoft Foundry / Azure OpenAI, Container Apps, Managed Identity, Key Vault, private endpoints. A: 🔐 Lab, cloud misconfiguration lab
- [ ] **Day 63:** CI/CD (GitHub Actions): tests + **eval gates + red-team gates**, OIDC to cloud (no long-lived secrets), canary deploys. A: DSA, mixed review
- [ ] **Day 64:** AI gateway: APIM AI gateway / LiteLLM, token-based rate limits, retries, circuit breakers, fallback models. A: 🔐 Lab, rate-limit bypass lab
- [ ] **Day 65:** Caching & latency: prompt caching, semantic caching (and **cross-tenant cache leakage**), streaming, async queues. A: DSA, mixed review
- [ ] **Day 66:** Observability: OTel GenAI traces, p50/p95/p99, cost per request, **security signals** (injection attempts, anomalous tool calls) → alerts. A: 🔐 Lab, detection-engineering exercise
- [ ] **Day 67:** Cost: model routing (small vs large), batch APIs, prompt compression, FinOps dashboards. A: DSA, mixed review
- [ ] **Day 68:** 🎯 Load test (k6/locust) + **SD #7:** observability + cost-aware routing layer for an LLM platform. A: 🔐 Lab, CTF of your choice

**Phase 6 Completion:** 0% (0/8 days)

---

## 📅 Phase 7: ML Fundamentals & System Design (Days 69-71)

- [ ] **Day 69:** Classic ML crash course (bias-variance, regularization, ensembles, metrics, calibration) + anomaly detection on auth logs (Isolation Forest). A: DSA, mixed review
- [ ] **Day 70:** DL refresher (backprop, optimizers, normalization) + ML system design framework on **fraud/abuse detection**. A: 🔐 Lab, review weakest lab category
- [ ] **Day 71:** 🎯🎯 Two timed mocks: (1) GenAI-security prompt, (2) agent-marketplace prompt. A: DSA, weakest pattern

**Phase 7 Completion:** 0% (0/3 days)

---

## 📅 Phase 8: Capstone: Secure Agent Marketplace (Days 72-76)

- [ ] **Day 72:** Architecture + full threat model (MAESTRO/STRIDE) + scope cut
- [ ] **Day 73:** Core build: registry, discovery, 2-3 hardened first-party agents (MCP + A2A)
- [ ] **Day 74:** Integration: identity/delegation, metered calls, vetting pipeline, observability
- [ ] **Day 75:** Red-team your own capstone → fix → re-run (publish the numbers)
- [ ] **Day 76:** Deploy, docs, demo video, written case study

**Phase 8 Completion:** 0% (0/5 days)

- [ ] 🛟 **Day 77:** Buffer: polish capstone / catch up

---

## 📅 Phase 9: Interview Sprint (Days 78-80)

- [ ] **Day 78:** Resume/portfolio/LinkedIn for AI Engineer × AI Security × agent platform roles; 6 STAR stories
- [ ] **Day 79:** Full mock loop: coding + GenAI/security system design + AI-security deep dive + behavioral
- [ ] **Day 80:** Gap-fill, final cheat-sheet review, rest

**Phase 9 Completion:** 0% (0/3 days)

---

## 📊 Statistics

- **Total Days Completed:** 0 / 80
- **Overall Progress:** 0%
- **Current Streak:** 0 days · **Longest Streak:** 0 days
- **DSA Problems Solved:** 0 (target ~60)
- **Security Labs Completed:** 0 (target ~35)
- **System Design Reps:** 0 / 9

---

## 💡 Key Learnings

### Phase 0
- *To be filled as you progress*

---

## 🎯 Milestones

- [ ] From-scratch attention + BPE by Day 8
- [ ] Secure LLM gateway skeleton by Day 16
- [ ] Secure RAG with eval + injection suite by Day 25
- [ ] Multi-agent system over MCP + A2A by Day 37
- [ ] Red-team report with before/after numbers by Day 50
- [ ] Mini agent marketplace v0 by Day 60
- [ ] Deployed with eval/red-team CI gates by Day 68
- [ ] Capstone launched by Day 76
- [ ] Full mock loop done by Day 79

---

## 📝 Notes

Log insights, blockers and breakthroughs here. These become your interview stories.
v1 history (Days 1-10, July-Sept 2026) lives in [archive/v1/](archive/v1/).

---

**Last Updated:** November 10, 2026
