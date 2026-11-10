# Phase 6: Production Platform: Deploy, Reliability, Cost (Days 61-68)

v1 spent 22 days on Azure, reliability and cost (archived in
[../archive/v1/phase_04_azure_deployment/](../archive/v1/phase_04_azure_deployment/),
[phase_05_reliability_scaling/](../archive/v1/phase_05_reliability_scaling/) and
[phase_06_cost_optimization/](../archive/v1/phase_06_cost_optimization/)). v2 compresses them to 8 days and adds what
v1 lacked: **evals and red-team suites as CI gates**, and **security signals in observability**.
Use the v1 READMEs as extra reading on any day you want more depth.

> ⚠️ **Verify current naming:** Azure AI Foundry was rebranded **Microsoft Foundry**. Check current
> product names and quota models in the Azure docs.

## Days

- **Day 61: Docker for AI apps.** Multi-stage builds, non-root user, minimal/distroless base, pinned digests,
  no secrets in layers, image scanning with [Trivy](https://github.com/aquasecurity/trivy).
- **Day 62: Azure deployment.** Microsoft Foundry / Azure OpenAI deployments & quotas, Container Apps,
  **Managed Identity** (no keys), Key Vault, private endpoints, Azure AI Search (optional).
- **Day 63: CI/CD.** GitHub Actions: lint → tests → **eval gate** (quality must not regress) → **red-team gate**
  (attack success rate must not rise) → build → scan → deploy; **OIDC federation to Azure** (no long-lived secrets);
  canary/blue-green.
- **Day 64: AI gateway & resilience.** APIM AI gateway or LiteLLM: token-based rate limits, retries with jitter,
  timeouts, circuit breakers, fallback models, graceful degradation.
- **Day 65: Caching & latency.** Provider prompt caching, semantic caching (and 🔐 **cross-tenant cache leakage**:
  key caches by tenant + permission set), streaming, async queues for long agent tasks.
- **Day 66: Observability.** OTel GenAI traces end-to-end (gateway → agent → MCP tools), p50/p95/p99, tokens & cost
  per request, and 🔐 security signals: guardrail hits, injection-classifier scores, anomalous tool-call sequences,
  denied authorizations → alerts.
- **Day 67: Cost optimization.** Small-vs-large model routing, batch APIs, prompt compression, cache hit-rate
  targets, FinOps dashboard and budget alerts.
- **Day 68: 🎯 Load test + SD #7.** k6/locust load test against the deployed system; publish latency/cost/error
  numbers. **SD #7:** *Observability + cost-aware routing layer for an LLM platform.*

## Resources

- [Azure OpenAI / Foundry docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/) · [Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/)
- [OpenTelemetry](https://opentelemetry.io/docs/) · [k6](https://k6.io/docs/) · [Locust](https://docs.locust.io/)

## Deliverable

Your Phase 3-5 system live on Azure behind the AI gateway, deployed by a pipeline with eval + red-team gates,
with a dashboard showing latency, cost and security signals under load.
