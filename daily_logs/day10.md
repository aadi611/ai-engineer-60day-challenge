Day 10   - March 4, 2026

Topics Covered
	•	Integrating tool usage within agent workflows (APIs/functions)
	•	Designing executor with tool-calling capability
	•	Parallel execution of independent tasks
	•	Improving validator with scoring-based evaluation

What I Learned
	•	Executors become significantly more powerful when augmented with tools (APIs, functions, DB calls)
	•	Not all steps need sequential execution — parallelism reduces latency
	•	A scoring-based validator provides better feedback than binary pass/fail
	•	Tool selection logic should be explicit to avoid unnecessary calls
	•	Structured outputs become even more critical when tools are involved

Code/Projects
	•	Extended executor to support tool usage:
	•	Function calling for specific tasks (e.g., data fetch, transformation)
	•	Implemented parallel execution for independent planner steps
	•	Upgraded validator:
	•	Added scoring system (0–10 scale)
	•	Included feedback for improvement
	•	Tested pipeline with:
	•	Multi-step tasks involving both reasoning + tool calls

Challenges
	•	Managing dependencies between parallel and sequential steps
	•	Preventing unnecessary or incorrect tool usage by executor
	•	Designing a meaningful scoring system for validator
	•	Handling tool failures gracefully within workflow

Resources
	•	OpenAI function/tool calling documentation
	•	LangChain tools and agents guide
	•	Articles on parallel processing in AI pipelines

Tomorrow’s Plan
	•	Add logging and observability (tracking each agent decision)
	•	Optimize latency and reduce redundant steps
	•	Introduce caching for repeated tool calls
	•	Test with more complex real-world scenarios