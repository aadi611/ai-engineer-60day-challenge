# Day 20 - March 12, 2026

## Topics Covered
- Human-in-the-loop (HITL) checkpoints for agentic workflows
- Confidence scoring and escalation logic for unsafe/uncertain outputs
- End-to-end observability with traces, spans, and structured logs
- FastAPI integration strategy for productionizing orchestrated agents

## What I Learned
- HITL checkpoints are most effective when triggered by explicit policies (low confidence, policy flags, or tool failures), not ad-hoc manual review
- Confidence should combine multiple signals: retrieval quality, answer grounding checks, and validator outcomes, rather than relying on a single model score
- Good observability for agent systems requires correlation IDs across the full request lifecycle so logs, traces, and retries can be reconstructed reliably
- Streaming intermediate states improves transparency for users and helps debug orchestration bottlenecks earlier
- Production APIs for agent workflows should separate synchronous quick responses from asynchronous long-running tasks with clear status endpoints

## Code/Projects
- Added a HITL decision gate in the supervisor workflow with a rule-based trigger for escalation
- Implemented a basic confidence aggregator that merges retrieval score, grounding check status, and validator pass/fail into one thresholded signal
- Added structured logging fields (`request_id`, `workflow_id`, `agent_name`, `step`, `latency_ms`) to each major orchestration step
- Prototyped a FastAPI endpoint pattern for running the workflow and returning step-wise progress metadata
- Created test cases for three paths: auto-approve, escalate-to-human, and fail-safe fallback response

## Challenges
- Setting confidence thresholds without over-escalating routine queries or under-escalating risky responses
- Designing HITL UX so reviewers get enough context quickly without reading full internal traces
- Keeping logs informative while avoiding excessive token-heavy payloads in debug output
- Managing branching complexity as orchestration adds more conditional paths and retries

## Resources
- LangGraph docs on conditional routing and checkpointing
- FastAPI docs for background tasks and response models
- OpenTelemetry guides for distributed tracing and correlation IDs
- Reliability engineering notes on escalation policies and incident triage

## Tomorrow's Plan
- Add LangSmith tracing across all agent transitions and tool invocations
- Introduce persistence for workflow checkpoints (Redis/Postgres) to support resume and auditability
- Build a lightweight reviewer dashboard view for escalated HITL cases
- Begin load-testing the orchestration API to establish baseline latency and throughput
