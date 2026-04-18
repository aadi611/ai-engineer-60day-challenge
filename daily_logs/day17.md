# Day 17 - March 9, 2026

## Topics Covered
- Agent memory systems and memory hierarchy design
- Short-term vs long-term memory in orchestration workflows
- Vector-based memory stores for retrieving past context
- Persisting useful state without storing every raw interaction

## What I Learned
- Memory works best when it is scoped and intentional instead of treating every message as permanent context
- Short-term memory should stay lightweight so the active workflow remains fast and debuggable
- Long-term memory is most useful when it stores distilled facts, preferences, and reusable summaries
- Retrieval quality matters as much as storage design because irrelevant memory can confuse downstream agents
- Good memory design improves continuity across sessions without bloating the working state

## Code/Projects
- Sketched the short-term memory module for session-level context retention
- Drafted the vector memory store for storing and retrieving durable notes
- Mapped how agent state can write to memory after important milestones
- Tested the idea of summarizing interactions before persisting them to long-term storage

## Challenges
- Deciding what should stay in active state versus what should be written to memory
- Avoiding duplicate or low-value memory entries
- Keeping retrieval targeted so the agent does not surface too much irrelevant history
- Balancing persistence with simplicity in the overall workflow design

## Resources
- Articles on agent memory architecture
- Vector database and semantic retrieval references
- LangGraph memory and checkpointing examples
- Notes on memory-scoped versus workflow-scoped state

## Tomorrow's Plan
- Build multi-agent collaboration patterns
- Define clear agent roles and handoff rules
- Connect memory retrieval to specialized agent workflows
- Evaluate how memory affects summarization and validation quality
