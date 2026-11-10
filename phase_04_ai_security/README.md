# Phase 4: AI Security: Attack & Defend (Days 39-50)

The differentiator. You attack the agent you built in Phase 3, measure how often the attacks succeed, harden it
and measure again. One rule runs through the phase: **prompt injection is not solved by a better prompt.** It is
contained by architecture: least agency, separated privileges, deterministic checks and humans on risky actions.

> ⚠️ **Verify current status:** OWASP publishes and revises these lists often. Check
> [genai.owasp.org](https://genai.owasp.org/) for the current LLM Top 10, the
> [Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
> (ASI01-ASI10, e.g. *Agent Goal Hijack*, *Tool Misuse*, built around **least agency**) and the **OWASP MCP Top 10**.

## Days

- **Day 39: Threat landscape & frameworks.** [OWASP Top 10 for LLM Apps (2025)](https://genai.owasp.org/llm-top-10/),
  OWASP Agentic Top 10, OWASP MCP Top 10, [MITRE ATLAS](https://atlas.mitre.org/), CSA **MAESTRO** (layered threat
  modeling for agentic AI). Re-do your Phase 3 threat model with these.
- **Day 40: Prompt injection & jailbreaks.** Direct vs indirect, role-play/encoding/many-shot/multi-turn (Crescendo)
  jailbreaks, invisible-Unicode smuggling, and Simon Willison's
  **[lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)**: private data + untrusted
  content + an exfiltration channel. Attack your Phase 3 agent by hand.
- **Day 41: Injection-resistant design.** Dual-LLM (privileged/quarantined), **[CaMeL](https://arxiv.org/abs/2503.18813)**
  (capabilities + data-flow tracking), and the six patterns from
  [*Design Patterns for Securing LLM Agents against Prompt Injections*](https://arxiv.org/abs/2506.08837)
  (action-selector, plan-then-execute, map-reduce, dual LLM, code-then-execute, context minimization). Plus spotlighting.
  Refactor one agent flow to plan-then-execute.
- **Day 42: Guardrails & classifiers.** Llama Guard / Prompt Guard, NeMo Guardrails, output filters, allow-listed
  links. **Measure FPR and FNR.** A guardrail you never measured is an unknown, not a control.
- **Day 43: Agent & tool security.** Excessive agency, confused deputy, least-privilege tool scopes, per-tool
  allow-lists, HITL for irreversible actions, egress allow-lists, secrets kept out of context, **sandboxing**
  (containers + seccomp, gVisor, Firecracker microVMs, hosted code sandboxes).
- **Day 44: MCP security.** Tool poisoning (malicious instructions in tool descriptions), **rug pulls** (tool
  definition changes after approval), tool shadowing across servers, cross-server data exfiltration, token
  passthrough, session hijacking, OAuth discovery SSRF, malicious local servers. Defenses: pin + hash tool
  definitions, re-consent on change, per-server isolation, scanning. Lab: *Damn Vulnerable MCP Server*.
- **Day 45: Automated red teaming.** [garak](https://github.com/NVIDIA/garak), [PyRIT](https://github.com/Azure/PyRIT),
  [promptfoo red team](https://www.promptfoo.dev/docs/red-team/). Build an attack suite and run it in CI (it becomes a gate in Phase 6).
- **Day 46: Model & data supply chain.** Pickle deserialization RCE vs safetensors, malicious HF repos, model
  signing ([OpenSSF model signing / Sigstore](https://github.com/sigstore/model-transparency)), data poisoning,
  backdoors ([Sleeper Agents](https://arxiv.org/abs/2401.05566)), AI-BOMs.
- **Day 47: Privacy attacks.** Membership inference, training-data extraction, model extraction/distillation,
  system-prompt leakage (and why the system prompt is not a secret store), differential privacy basics.
- **Day 48: Governance & compliance.** [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) +
  [GenAI Profile (AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf),
  [EU AI Act](https://artificialintelligenceact.eu/) (risk tiers, GPAI obligations, timelines; *verify current dates*),
  [ISO/IEC 42001](https://www.iso.org/standard/81230.html), SOC 2 for AI products, AI incident response.
- **Day 49: AI for security (defender side).** SOC alert-triage agent, log-analysis RAG over your Phase 1 audit
  logs, threat-intel RAG, vuln-finding agents (DARPA AIxCC lessons), and the guardrails such tools themselves need.
- **Day 50: 🎯 Ship + SD #5.** **Red-team report** on your Phase 3 system: scope, method, findings (mapped to
  OWASP/ATLAS IDs), attack success rate **before → after** hardening, residual risk.
  **SD #5:** *Design an enterprise AI firewall / guardrail service.*

## Labs used this phase

[Gandalf](https://gandalf.lakera.ai/) · [PortSwigger Web LLM attacks](https://portswigger.net/web-security/llm-attacks) ·
Dreadnode Crucible · Damn Vulnerable MCP Server · see [../security_labs/](../security_labs/README.md)

## Deliverables

- `redteam/` (garak/PyRIT/promptfoo configs + results), `REDTEAM_REPORT.md`, hardened agent v2
- SD #5 write-up. **This report is your strongest portfolio artifact for AI-security roles.**
