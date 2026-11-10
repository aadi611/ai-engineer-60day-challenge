# System Design Track (v2)

One 🎯 rep per phase (see [../progress_tracker.md](../progress_tracker.md)). 45-60 min timed, then a write-up here.
The v1 version of this README is in [../archive/v1/system_design_README.md](../archive/v1/system_design_README.md).

## Framework (v2 adds step 6)

1. **Clarify requirements:** functional and non-functional (latency, scale, cost, consistency)
2. **Back-of-envelope:** QPS, tokens/sec, storage, $/day
3. **High-level architecture:** draw it, name every component
4. **Deep dive on 2-3 components:** where the interviewer actually wants to go
5. **Bottlenecks & tradeoffs:** what breaks at 10x?
6. **🔐 Threat model:** trust boundaries, untrusted inputs (users, documents, tools, other agents), the lethal-trifecta
   check, blast radius of a compromised agent/tool, authZ at every hop
7. **Monitoring & failure modes:** what pages you at 3 a.m., including security alerts

## The 9 reps

| Day | Prompt | File |
|---|---|---|
| 8 | Low-latency LLM inference service | `01_llm_inference_service.md` |
| 16 | Secure multi-tenant LLM API gateway | `02_secure_llm_gateway.md` |
| 25 | RAG for 10M docs, <500 ms p99, per-user permissions | `03_permission_aware_rag.md` |
| 37 | Multi-agent customer-support platform | `04_multiagent_support.md` |
| 50 | Enterprise AI firewall / guardrail service | `05_ai_firewall.md` |
| 60 | Agent marketplace: 10k agents / 1M users (discovery, trust, payments) | `06_agent_marketplace.md` |
| 68 | Observability + cost-aware routing layer | `07_observability_routing.md` |
| 71 | Mock #1: GenAI-security prompt (timed) | `mock_01.md` |
| 71 | Mock #2: marketplace prompt (timed) | `mock_02.md` |

## Prompt bank (extra reps)

- Design ChatGPT-like product / semantic search at scale (from v1)
- Design prompt-injection defense for an email assistant with send permissions
- Design the vetting pipeline for a public MCP registry
- Design sandboxed code execution for 100k agent sessions/day
- Design delegated payments for a shopping agent (consent, limits, disputes)
- Design a SOC alert-triage agent with human escalation
- Design a model-serving platform with signed-model supply chain

Each write-up: problem, diagram (ASCII or image), tradeoffs, threat model, and **what you'd say differently next time**.
