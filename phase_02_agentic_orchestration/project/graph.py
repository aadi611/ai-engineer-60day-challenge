"""LangGraph wiring: supervisor fans out to category specialist agents (parallel),
then fans back in for final report synthesis.

"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.constants import Send

from agents import run_category_scout, write_final_report
from categories import CATEGORIES, resolve_categories
from state import JobState


def route_categories(state: JobState) -> list[Send]:
    """Fan-out: dispatch one Send per requested category to the scout node."""
    categories = resolve_categories(state["categories"])
    return [
        Send("scout", {**state, "categories": [c.key]})
        for c in categories
    ]


def scout_node(state: JobState) -> dict:
    """Run a single category's specialist agent (search + extract)."""
    category = CATEGORIES[state["categories"][0]]
    leads, summary = run_category_scout(category, state["city"], state.get("budget_note", ""))
    return {"leads": leads, "category_summaries": [summary]}


def supervisor_node(state: JobState) -> dict:
    """Fan-in: synthesize all specialist summaries into the final report."""
    report = write_final_report(state["city"], state["category_summaries"], state["leads"])
    return {"final_report": report}


def build_graph():
    graph = StateGraph(JobState)
    graph.add_node("scout", scout_node)
    graph.add_node("supervisor_report", supervisor_node)

    graph.add_conditional_edges(START, route_categories, ["scout"])
    graph.add_edge("scout", "supervisor_report")
    graph.add_edge("supervisor_report", END)

    return graph.compile()
