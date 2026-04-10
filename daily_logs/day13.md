Day 13 - March 5, 2026

Topics Covered
	•	Logging and observability in multi-agent workflows
	•	Cost tracking (tokens, API usage, tool calls)
	•	Planner enhancement with dependency graph representation
	•	Caching strategies for repeated queries and responses
	•	Introduction to production-level scalability concepts

⸻

What I Learned
	•	Observability is critical for debugging complex agent workflows and understanding failure points
	•	Fine-grained logging (per step) makes it easier to trace planner → executor → validator flow
	•	Tracking token and API costs helps in optimizing system efficiency and budgeting
	•	Representing plans as dependency graphs improves execution clarity and enables smarter parallelism
	•	Caching reduces redundant computation and significantly improves response time
	•	Scalability requires thinking beyond correctness — performance, cost, and reliability matter equally

⸻

Code/Projects
	•	Implemented structured logging:
	•	Logged each step’s input, output, execution time, and status
	•	Added trace IDs to track full workflow execution
	•	Added cost tracking module:
	•	Calculated token usage per LLM call
	•	Tracked API/tool usage cost separately
	•	Enhanced Planner:
	•	Converted linear plans into dependency graphs (DAG-like structure)
	•	Tagged steps as dependent/independent for better execution planning
	•	Built caching layer:
	•	Stored repeated LLM responses using hash-based keys
	•	Implemented cache invalidation strategies
	•	Improved Executor:
	•	Integrated logging + cost tracking within execution pipeline
	•	Tested scenarios:
	•	Repeated queries (to validate caching efficiency)
	•	Complex workflows with multiple dependencies
	•	Cost vs performance trade-offs

⸻

Challenges
	•	Designing a clean logging structure without cluttering output
	•	Accurately estimating token usage across different models/tools
	•	Handling cache invalidation without breaking correctness
	•	Representing dynamic workflows as graphs without overcomplicating the planner
	•	Balancing caching vs freshness of responses

⸻

Resources
	•	OpenTelemetry basics for observability
	•	Articles on DAG-based workflow systems
	•	Redis / in-memory caching concepts
	•	OpenAI pricing & token usage docs
	•	System design resources on scalable architectures

⸻

Tomorrow’s Plan
	•	Implement retry strategies with exponential backoff
	•	Add fault tolerance for partial workflow failures
	•	Introduce queue-based execution (e.g., task queues)
	•	Improve validator with contextual feedback (not just scoring)
	•	Start preparing a clean architecture diagram for the entire system 🚀