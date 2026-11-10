# Home Services Vendor Finder (Multi-Agent)

Day 24 deliverable for [Phase 2: Agentic Systems & Orchestration](../README.md).

Finds budget-friendly vendors/contractors in India for home-service jobs —
wall revamp, WPC panels, carpentry, plumbing, electrical, painting — by running
one specialist search agent per category in parallel, then having a supervisor
agent synthesize everything into a single comparison report.

## Architecture

```
START
  |
  v
route_categories (supervisor: fan-out)
  |
  +--> scout[wall_revamp]   --\
  +--> scout[wpc_panels]     |
  +--> scout[carpenter]      +--> supervisor_report (fan-in) --> END
  +--> scout[plumber]        |
  +--> scout[...]           -/
```

- **Specialist agents** (`scout` node, one instance per category, run in
  parallel via LangGraph `Send`): each does a ReAct-style loop — call the
  Tavily web search tool with category-specific queries, then use GPT-4o
  tool-calling to extract structured `VendorLead` records (name, price,
  location, source, notes) from the raw results.
- **Supervisor agent** (`supervisor_report` node): fans in all specialist
  summaries + raw leads and writes one markdown report with per-category
  comparison tables and budget tips.
- **State** (`state.py`): a shared `JobState` TypedDict; `leads` and
  `category_summaries` use `Annotated[..., operator.add]` so parallel
  branches merge without clobbering each other.

## Setup

```bash
cd phase_02_agentic_orchestration/project
pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY and TAVILY_API_KEY
```

Get a free Tavily API key at https://tavily.com (used for live web search).

## Usage

```bash
python main.py --city "Bengaluru" --categories wall_revamp,plumber,carpenter
python main.py --city "Pune" --categories "wpc panels" --budget "under 15000 total"
```

Available categories: `wall_revamp`, `wpc_panels`, `carpenter`, `plumber`,
`electrician`, `painter` (see `categories.py` — add more by adding entries
to the `CATEGORIES` dict, no graph changes needed).

## Extending

- **New category**: add an entry to `CATEGORIES` in `categories.py` with
  search hints. No other code changes needed.
- **New data source** (e.g. a vendor API instead of/alongside web search):
  add a tool function in `agents.py` and bind it alongside `_extract_tool`.
- **Human-in-the-loop**: add an `interrupt()` before `supervisor_report` to
  let the user drop/edit leads before the final report is generated.
