# Phase 3: Agents, Context Engineering & Protocols (Days 26-37)

The core of the "agent marketplace expert" profile. Agents in a marketplace are built in one place, discovered
in another and invoked by a third party. **MCP** (agent ↔ tools/data) and **A2A** (agent ↔ agent) are the plumbing
for that, so this phase goes deep on both.

> **v1 reference:** [../archive/v1/phase_02_agentic_orchestration/project/](../archive/v1/phase_02_agentic_orchestration/project/)
> is your LangGraph fan-out vendor-scout agent (`Send` API, Tavily). Reuse it on Day 29 as the LangGraph example.

> ⚠️ **Verify current status:** MCP has had major spec revisions (the 2026 revision moved toward a stateless core).
> Read the **current** spec at modelcontextprotocol.io, not a 2025 tutorial. MCP is now governed by the Linux
> Foundation's [Agentic AI Foundation](https://aaif.io/).

## Days

- **Day 26: Agent loop from scratch.** No framework: a `while` loop, tool schemas, tool execution, ReAct-style
  reasoning, max-steps/stop conditions, error handling. Then: workflows (prompt chaining, routing, parallelization,
  orchestrator-workers, evaluator-optimizer) vs autonomous agents.
- **Day 27: Context engineering.** Tool design as an agent-computer interface (names, descriptions, error messages),
  just-in-time retrieval vs up-front stuffing, compaction, structured note-taking, sub-agents for context isolation.
- **Day 28: Agent SDKs side by side.** Build the same small agent with the **Claude Agent SDK**, the **OpenAI Agents SDK**
  and **LangGraph**. Compare tool definition, handoffs, guardrails, tracing and permission models.
- **Day 29: LangGraph deep dive.** State, reducers, checkpointers, `interrupt` for human-in-the-loop, durable
  execution, time travel. Revisit your v1 vendor-scout graph.
- **Day 30: Multi-agent patterns.** Orchestrator-workers, supervisor, handoffs, swarm. The cost and latency of
  multi-agent systems, and when a single agent with better tools wins.
- **Day 31: Memory.** Short-term (context), long-term (vector/kv/graph), episodic vs semantic, memory tools.
  🔐 **Memory poisoning:** one injected instruction persisted into memory compromises every future session.
- **Day 32: MCP I: build.** An MCP server with the official Python SDK (tools, resources, prompts), stdio vs
  Streamable HTTP transport, an MCP client, and plugging your server into an agent and into Claude.
- **Day 33: MCP II: production features.** Authorization (OAuth 2.1, protected resource metadata, resource
  indicators, **no token passthrough**), elicitation, structured tool output, the official **MCP Registry**
  (`server.json`), and **Agent Skills** (packaged instructions + scripts loaded on demand).
- **Day 34: A2A.** [A2A protocol](https://a2a-protocol.org/): agent cards (discovery), tasks, messages/artifacts,
  streaming, push notifications. MCP vs A2A: *tools vs peers*. Expose your Day 30 agent over A2A.
- **Day 35: Computer-use & code-execution agents.** Browser/desktop agents, code interpreters, why they need
  sandboxes (preview of Day 43), and why web content is untrusted input.
- **Day 36: Agent evals & observability.** Final-answer vs trajectory evals, tool-call accuracy, task success
  rate, cost per task; benchmarks (SWE-bench, τ-bench style); [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/);
  Langfuse / LangSmith tracing.
- **Day 37: 🎯 Ship + SD #4.** Multi-agent system: 2-3 specialist agents, tools served over **MCP** (your server),
  orchestrator exposed over **A2A**, HITL approval on one risky action, full traces, eval suite.
  **SD #4:** *Multi-agent customer-support platform.*

## Resources

- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Model Context Protocol](https://modelcontextprotocol.io/) (spec, SDKs, security best practices, registry)
- [MCP Registry](https://registry.modelcontextprotocol.io/)
- [A2A Protocol](https://a2a-protocol.org/)
- [Agent Skills](https://agentskills.io/)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) · [LangGraph](https://langchain-ai.github.io/langgraph/) · Claude Agent SDK (in the [Anthropic docs](https://docs.claude.com/))

## Deliverables

- `agent_from_scratch.py`, a 3-SDK comparison note, `mcp_server/`, an A2A-exposed orchestrator
- Phase 3 ship project + eval report + SD #4 write-up
- `threat_models/phase3_agent.md`, a first-pass threat model that you'll attack in Phase 4
