



Day 11
- March 4, 2026

Topics Covered
	•	Tool integration within Executor (APIs, function calling, external services)
	•	Parallel execution of independent tasks in multi-agent workflows
	•	Enhanced Validator with scoring mechanism (instead of binary pass/fail)
	•	Performance benchmarking across different workflow complexities



What I Learned
	•	Integrating tools (APIs/functions) makes agents significantly more powerful and practical
	•	Parallel execution reduces latency and improves efficiency for independent steps
	•	A scoring-based validator provides better insights than simple pass/fail
	•	Benchmarking helps identify bottlenecks in planner, executor, or validator stages
	•	Not all tasks benefit from parallelism — dependency mapping is crucial



Code/Projects
	•	Extended Executor to:
	•	Call external APIs and internal utility functions
	•	Dynamically decide whether a step needs a tool or LLM execution
	•	Implemented parallel execution:
	•	Identified independent steps in planner output
	•	Used async processing to execute them simultaneously
	•	Upgraded Validator:
	•	Introduced scoring system (0–100) based on accuracy, completeness, and format
	•	Added threshold-based acceptance (e.g., ≥80 passes)
	•	Built benchmarking module:
	•	Measured execution time, retries, and success rate
	•	Compared sequential vs parallel workflows
	•	Tested scenarios:
	•	Multi-step tasks with mixed dependencies
	•	Tool-heavy vs LLM-heavy workflows
	•	Observed performance gains in parallel execution cases



Challenges
	•	Managing race conditions and synchronization in parallel execution
	•	Deciding when to trigger tools vs rely on LLM reasoning
	•	Designing a fair and consistent scoring system for validation
	•	Handling API failures within parallel flows
	•	Avoiding over-engineering for simple 

Resources
	•	Async programming patterns (Python asyncio / JS promises)
	•	OpenAI function/tool calling docs
	•	LangGraph parallel node execution concepts
	•	Articles on distributed systems & concurrency models



Tomorrow’s Plan
	•	Add logging and observability (trace each step clearly)
	•	Implement cost tracking (tokens + API usage)
	•	Improve planner with dependency graph visualization
	•	Introduce caching for repeated queries
	•	Start optimizing for production-level scalability 🚀

⸻

