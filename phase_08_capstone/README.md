# Phase 8: Capstone: Secure Agent Marketplace (Days 72-76)

One project that proves all three parts of the profile: **AI engineering** (agents, RAG, MCP/A2A, production),
**security** (threat model, red team, hardening with numbers), and **marketplace** (registry, vetting, identity,
delegation, metering). It grows out of your Phase 5 v0 and does not start from zero.

> v1's capstone idea (enterprise copilot) is archived in [../archive/v1/phase_07_capstone_copilot/](../archive/v1/phase_07_capstone_copilot/).
> You can still frame the marketplace around a concrete domain (e.g. *internal IT/SecOps agents marketplace for a
> company*). A specific use case demos better than a generic one.

## Scope (minimum)

1. **Registry & discovery:** submit/list/search agents and MCP servers with signed manifests
2. **Vetting pipeline:** static scan + tool-description injection scan + sandboxed dynamic run + red-team suite, with a published scorecard per listing
3. **2-3 first-party agents** (one RAG-backed, one tool-using with a HITL step) exposed over MCP and/or A2A
4. **Identity & delegation:** user → agent token exchange with scoped, short-lived tokens; full audit trail
5. **Metering:** per-call usage events → Stripe **test mode** billing
6. **Production:** deployed via the Phase 6 pipeline with eval + red-team gates, OTel dashboard with security signals

## Days

- **Day 72:** Architecture, full threat model (STRIDE + MAESTRO), scope cut. Write down what you will **not** build.
- **Day 73:** Core: registry, discovery, first-party agents.
- **Day 74:** Integration: identity/delegation, metering, vetting pipeline, observability.
- **Day 75:** Red-team your own capstone → fix → re-run. Publish the before/after numbers.
- **Day 76:** Deploy, README, 3-5 min demo video, written **case study** (problem → architecture → threats →
  tradeoffs → results → what you'd do next).

## Deliverable

A deployed, documented, demo-ready secure agent marketplace + case study + red-team report. You lead with this in every interview.
