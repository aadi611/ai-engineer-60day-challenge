# 🛡️ AI Engineer Challenge — v2: AI Engineering × Cybersecurity × Agent Marketplaces

**v2 restart.** v1 (the 60-day interview plan, started July 2026, stopped around Day 10) is
preserved in full under [archive/v1/](archive/v1/). Every file, log and line of code is kept. v2 starts from the basics
again and is re-aimed at a sharper target profile:

> **An AI Engineer who builds production agents, can break and defend them, and knows how
> agents are packaged, discovered, trusted and paid for in agent marketplaces.**

**Start Date:** 2026-11-11
**Target Completion:** ~late May 2027 (Day 80), re-dated for GATE 2027
**Commitment:** GATE mode until the exam (30 min/day), then ~2.5-3 hrs/day, 6 days/week · 2 built-in 🛟 buffer days

> ## 🎓 GATE mode (Nov 11, 2026 → GATE RA exam, Feb 2027)
> GATE 2027 (Robotics & Automation) comes first. Until the exam, this plan runs at **maintenance pace**:
> 30 min/day on Phase 0 (Days 1-8), DSA or a lab, plus a daily commit. Full GATE plan: **[gate_prep/](gate_prep/README.md)**.
> After the exam, the plan resumes at full pace from **Day 9** (~Feb 22, 2027).

---

## 🧭 How each day works (three tracks)

| Block | Time | What |
|---|---|---|
| **A — Skills rep** | ~45 min | **Odd days:** DSA problem(s) ([dsa_practice/](dsa_practice/README.md)). **Even days:** hands-on security lab ([security_labs/](security_labs/README.md)) |
| **B — Core build** | ~2-2.5 hrs | That day's phase topic: theory + hands-on implementation |
| **C — Systems & security lens** | ~30-45 min | Reading, a threat-model note on what you built, or (on 🎯 days) a timed system-design rep |

Every build day ends with one question written into the daily log:
**"How would I attack what I built today?"** That habit is the whole point of v2.

---

## 📚 Phase Structure

| Phase | Days | Focus | Ship |
|---|---|---|---|
| [0 — Foundations](phase_00_foundations/README.md) | 1-8 | Modern Python, LLM APIs, transformer internals, reasoning models, inference | From-scratch attention + BPE, inference SD |
| [1 — Security Foundations](phase_01_security_foundations/README.md) | 9-16 | Threat modeling, web/API security, OAuth/OIDC, crypto, cloud, supply chain | Secure LLM API gateway skeleton |
| [2 — Secure Production RAG](phase_02_secure_rag/README.md) | 17-25 | Retrieval internals, hybrid + rerank, permission-aware RAG, RAG attacks, evals | RAG with ACLs + eval + injection tests |
| [3 — Agents, Context Engineering & Protocols](phase_03_agents_protocols/README.md) | 26-37 | Agent loops, agent SDKs, LangGraph, memory, **MCP**, **A2A**, Agent Skills, computer use, agent evals | Multi-agent system over MCP + A2A |
| 🛟 Buffer + midpoint retro | 38 | Catch up, re-plan | — |
| [4 — AI Security: Attack & Defend](phase_04_ai_security/README.md) | 39-50 | OWASP LLM / Agentic / MCP Top 10s, MITRE ATLAS, prompt injection, secure agent design, red teaming, supply chain, governance | Red-team report + hardened agent |
| [5 — Agent Marketplaces & Agentic Commerce](phase_05_agent_marketplace/README.md) | 51-60 | Registries, packaging, discovery, agent identity, delegation, agent payments (AP2/ACP/UCP/x402), metering, marketplace trust & safety | Mini agent marketplace v0 |
| [6 — Production Platform](phase_06_production_platform/README.md) | 61-68 | Docker, Azure, CI/CD with eval + red-team gates, AI gateway, caching, observability, cost | Deployed, observable, cost-routed |
| [7 — ML Fundamentals & System Design](phase_07_ml_system_design/README.md) | 69-71 | Classic ML/DL refresher (security-flavoured), ML design, 2 timed mocks | 2 mock write-ups |
| [8 — Capstone: Secure Agent Marketplace](phase_08_capstone/README.md) | 72-76 | Integrate everything into one portfolio project | Deployed capstone + case study |
| 🛟 Buffer | 77 | Catch up / polish | — |
| [9 — Interview Sprint](phase_09_interview_sprint/README.md) | 78-80 | Resume, STAR stories, full mock loop | Interview-ready |

Day-by-day checklist: **[progress_tracker.md](progress_tracker.md)**.

---

## 🆕 What changed from v1 (and why)

| v1 | v2 |
|---|---|
| Security was one day (Day 23) + one Azure day | A full **security foundations** phase (Phase 1), plus a full **AI security** phase (Phase 4). Every phase has a security lens. |
| Agents = LangGraph + a mention of MCP | Framework-free agent loop first, then Claude Agent SDK / OpenAI Agents SDK / LangGraph, **context engineering**, **MCP in depth (incl. auth)**, **A2A**, **Agent Skills**, computer-use agents, agent evals |
| No marketplace / commerce content | A full **agent marketplace & agentic commerce** phase: registries, discovery, identity, delegation, payments, metering, trust & safety |
| Capstone: generic enterprise copilot | Capstone: **secure agent marketplace** (registry + vetting pipeline + hardened agents + metered calls) |
| Track A: DSA every day | Track A alternates **DSA** and **security labs** (PortSwigger, Gandalf, Juice Shop, CTFs) |
| Reasoning models absent | Reasoning models, test-time compute, RLVR/GRPO, MoE, prompt caching, structured outputs |
| Phases 4-6 (Azure, reliability, cost) = 22 days | Compressed into one 8-day production phase that adds **eval & red-team gates in CI** and **security observability** |

### New concepts added to the material (Nov 2026 refresh)

- **Agent protocols & standards:** MCP (latest stable spec revision, stateless core, OAuth-based authorization, official MCP Registry), now governed by the Linux Foundation's **Agentic AI Foundation (AAIF)**. Also **A2A** (agent cards, tasks), **Agent Skills**, and AGENTS.md.
- **AI security frameworks:** OWASP Top 10 for LLM Apps (2025), **OWASP Top 10 for Agentic Applications (2026)**, **OWASP MCP Top 10**, MITRE ATLAS, CSA MAESTRO, NIST AI RMF + GenAI Profile (AI 600-1), EU AI Act, ISO/IEC 42001.
- **Prompt-injection defense by design:** the lethal trifecta, Dual-LLM, CaMeL, and agent design patterns (plan-then-execute, action-selector, context minimization).
- **Agentic commerce:** AP2 (mandates), ACP (agent checkout), **UCP** (Universal Commerce Protocol), **x402** (HTTP 402 machine payments), and card-network agent programs.
- **Agent identity & trust:** workload identity, OAuth token exchange / on-behalf-of, signed manifests, Web Bot Auth / signed agents, "Know Your Agent".
- **Model supply chain:** safetensors vs pickle, model signing (OpenSSF/Sigstore), AIBOM, slopsquatting (hallucinated package names).

> ⚠️ This space moves monthly. Each phase README has a **"verify current status"** note on the
> fast-moving items. On those days, part of Track B is reading the primary spec, not a blog post.

---

## 🛠️ Tech Stack

- **AI/LLM:** Anthropic Claude API & Claude Agent SDK, OpenAI API & Agents SDK, LangGraph, HuggingFace, vLLM
- **Protocols:** MCP (Python SDK / FastMCP), A2A, OAuth 2.1 / OIDC
- **Security tooling:** garak, PyRIT, promptfoo, Llama Guard / Prompt Guard, Presidio, Semgrep, Bandit, Trivy, gitleaks, Burp Suite (Community)
- **Vector/Search:** pgvector, Qdrant/FAISS, BM25, cross-encoder rerankers
- **Backend:** Python 3.12+, FastAPI, Pydantic v2, `uv`
- **Cloud/Ops:** Azure (Microsoft Foundry / Azure OpenAI, Container Apps, Key Vault, APIM), Docker, GitHub Actions
- **Observability:** OpenTelemetry (GenAI semantic conventions), Langfuse/LangSmith, Prometheus/Grafana
- **Payments (test mode only):** Stripe test mode, x402 testnet

## Prerequisites

- Python 3.12+, `uv`, Docker
- Anthropic and/or OpenAI API key (keep in `.env`, never committed; see Day 1)
- Azure subscription (Phase 6+)
- Free accounts: LeetCode, PortSwigger Web Security Academy, TryHackMe (optional), Stripe (test mode)

## 📁 Project Structure

```
ai-engineer-60day-challenge/
├── phase_00_foundations/
├── phase_01_security_foundations/
├── phase_02_secure_rag/
├── phase_03_agents_protocols/
├── phase_04_ai_security/
├── phase_05_agent_marketplace/
├── phase_06_production_platform/
├── phase_07_ml_system_design/
├── phase_08_capstone/
├── phase_09_interview_sprint/
├── dsa_practice/            # Track A, odd days
├── security_labs/           # Track A, even days
├── system_design/           # weekly 🎯 design reps
├── daily_logs/              # v2 logs (day_01.md, ...)
├── gate_prep/               # GATE 2027 RA plan, syllabus tracker, mistake log, mocks
├── quant_trading/           # parallel self-paced track (unchanged)
├── archive/v1/              # ← the complete v1 plan, logs and code, untouched
└── progress_tracker.md
```

## 📈 Parallel Track: Quantitative Trading

Unchanged. A self-paced track (not on the clock). See [quant_trading/README.md](quant_trading/README.md).

## 🎯 Goals

- Explain transformer internals, reasoning models and inference optimization at interview depth
- Ship a permission-aware RAG system with a real eval and injection test suite
- Ship a multi-agent system exposed over MCP and A2A, traced and evaluated
- Red-team your own agent with garak/PyRIT/promptfoo, and show before/after numbers after hardening
- Explain and threat-model an agent marketplace: discovery, identity, delegation, payments, vetting
- Deploy on Azure with CI gates for evals and security, plus security-aware observability
- ~60 DSA problems + ~35 security labs
- Capstone: a **secure agent marketplace** you can demo in 5 minutes or defend for 60

---

**Current Phase:** 🎓 GATE mode + Phase 0 at maintenance pace (v2 Day 1 = 2026-11-11)
