# Phase 5: Agent Marketplaces & Agentic Commerce (Days 51-60)

An agent marketplace solves four hard problems at once: **discovery** (find the right agent/tool),
**trust** (is it safe and is it what it claims), **delegation** (acting for a user with bounded authority)
and **payment** (who pays whom, per call, with what proof of consent). This phase covers each one, and the
capstone puts them together.

> ⚠️ **Verify current status: this is the fastest-moving area in the plan.** As of late 2026, reported
> developments include: MCP and its official Registry under the Linux Foundation's Agentic AI Foundation;
> **AP2** (Google, human-authorization "mandates"; reportedly moved to the FIDO Alliance); **ACP** (OpenAI + Stripe,
> agent checkout); **UCP** (Universal Commerce Protocol, Google + Shopify, Jan 2026); **x402** (Coinbase's HTTP 402
> machine payments, now under a Linux Foundation x402 Foundation); and newer entrants such as MPP.
> Confirm each against its **primary spec** on the day you study it. Blog comparisons go stale within months.

## Days

- **Day 51: Landscape & business models.** Registries and stores: MCP Registry + sub-registries, ChatGPT apps
  (Apps SDK), Claude plugin/Skills marketplaces, AWS Marketplace "AI agents & tools", Microsoft agent store / Copilot
  Studio, Salesforce AgentExchange, Google Cloud agent offerings. Map each one's packaging format, discovery,
  review process, pricing model (free, subscription, usage-based, rev share) and liability split.
- **Day 52: Packaging & listing.** Manifests: MCP `server.json`, A2A agent card, plugin/skill manifests.
  Versioning and semver for tool schemas (a renamed parameter is a breaking change), capability and **permission
  declarations**, documentation that LLMs (not just humans) read. Publish your Phase 3 MCP server to a test/sub-registry.
- **Day 53: Discovery & ranking.** Semantic search over capability descriptions (reuse your Phase 2 RAG), tool
  search at runtime, ranking signals (eval scores, uptime, latency, ratings), and SEO/spam/**description-injection**
  gaming of the ranking itself.
- **Day 54: 🔐 Agent identity & trust.** Workload identity ([SPIFFE](https://spiffe.io/)), OAuth client credentials,
  signed manifests (reuse Day 12), **Web Bot Auth** / signed-agent HTTP message signatures, "Know Your Agent",
  verifiable credentials/DIDs. Answer: how does a merchant know which agent is calling and on whose behalf?
- **Day 55: 🔐 Delegated authorization.** [OAuth 2.0 Token Exchange (RFC 8693)](https://www.rfc-editor.org/rfc/rfc8693),
  on-behalf-of flows, down-scoped short-lived tokens, step-up consent, revocation, audit trails that record
  *user → agent → sub-agent → tool*. Multi-tenant isolation in a shared marketplace.
- **Day 56: 💳 Agent payments.** AP2 (intent/cart mandates as verifiable credentials), ACP (agent ↔ merchant checkout,
  delegated payment tokens), UCP, [x402](https://www.x402.org/) (pay-per-request over HTTP 402), card-network agent
  programs (e.g. Visa Intelligent Commerce, Mastercard Agent Pay). Fraud, disputes, liability.
  *Build with [Stripe test mode](https://docs.stripe.com/testing) / testnets only. No real money.*
- **Day 57: Metering, billing & economics.** Usage events at the gateway, idempotent metering, pricing (per call,
  per token, per outcome), quotas and spend caps per delegating user, rev-share accounting, cost attribution per agent call.
- **Day 58: 🔐 Marketplace trust & safety pipeline.** Automated vetting for submitted agents/MCP servers:
  static analysis (Semgrep, dependency + secret scans), **tool-description injection scan**, sandboxed dynamic run with
  egress monitoring, permission-vs-behaviour diff, red-team suite from Phase 4. Then: version pinning + hash
  verification against rug pulls, continuous monitoring, kill-switch/takedown, disclosure process.
- **Day 59: Cross-vendor interop.** A2A between agents from different vendors, contracts/SLAs, **evals as
  certification** (publishable scorecards), cross-org tracing, dispute handling when a third-party agent misbehaves.
- **Day 60: 🎯 Ship + SD #6.** **Mini agent marketplace v0:** registry API (submit/list/search), vetting pipeline
  (at least static + injection scan + sandbox run), signed manifests, delegated tokens, metered calls with Stripe
  test mode. **SD #6:** *Agent marketplace for 10k agents and 1M users: discovery, trust, payments.*

## Deliverables

- `marketplace/` (registry API, `vetting/`, `billing/`), a written threat model of the marketplace itself
- A "protocol map" cheat sheet: MCP · A2A · Skills · AP2 · ACP · UCP · x402 (what layer each owns and who governs it)
- SD #6 write-up
