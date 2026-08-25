"""Specialist and supervisor agent logic.

Pattern: supervisor (fan-out/fan-in) + N specialist agents, one per job category.
Each specialist agent does its own ReAct-style loop: call the web search tool,
then extract structured vendor leads from the results via tool calling.
"""

from __future__ import annotations
import time
import json
import os

from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from categories import Category
from state import VendorLead

MODEL_NAME = os.environ.get("AGENT_MODEL", "gpt-4o")

_tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

_extract_tool = {
    "name": "record_vendor_leads",
    "description": "Record structured vendor/pricing leads extracted from search results.",
    "input_schema": {
        "type": "object",
        "properties": {
            "leads": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Vendor, contractor, or platform name"},
                        "price_estimate": {"type": "string", "description": "Price or rate, with unit if known (e.g. 'Rs 45/sq ft')"},
                        "location": {"type": "string", "description": "City/area served, if known"},
                        "contact_or_source": {"type": "string", "description": "URL, phone, or platform where this was found"},
                        "notes": {"type": "string", "description": "Rating, caveats, budget-friendliness, anything notable"},
                    },
                    "required": ["name", "price_estimate", "contact_or_source"],
                },
            }
        },
        "required": ["leads"],
    },
}

_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)


def _web_search(query: str, max_results: int = 6) -> str:
    results = _tavily.search(query=query, max_results=max_results, include_answer=True)
    chunks = []
    if results.get("answer"):
        chunks.append(f"Summary: {results['answer']}")
    for r in results.get("results", []):
        chunks.append(f"- {r['title']}: {r['content'][:400]} (source: {r['url']})")
    return "\n".join(chunks) if chunks else "No results found."


def run_category_scout(category: Category, city: str, budget_note: str) -> tuple[list[VendorLead], str]:
    """Search + extract vendor leads for a single category. Returns (leads, human-readable summary)."""
    queries = [f"{hint} {city}" for hint in category.search_hints]
    queries.append(f"best budget friendly {category.label} in {city}")

    search_blobs = [_web_search(q) for q in queries]
    combined = "\n\n".join(
        f"Query: {q}\n{blob}" for q, blob in zip(queries, search_blobs)
    )

    prompt = f"""You are a vendor-scouting specialist for the category: {category.label}.
City: {city}
Budget preference: {budget_note or "no specific budget stated, prefer budget-friendly options"}

Below are web search results. Extract concrete vendor/contractor leads with price
estimates. Prefer budget-friendly, well-reviewed options. If prices are ranges,
keep the range. Skip vague or irrelevant results. Call record_vendor_leads with
what you find (3-6 leads is ideal; fewer is fine if that's all the data supports).

SEARCH RESULTS:
{combined}
"""

    response = _llm.bind_tools([_extract_tool], tool_choice="record_vendor_leads").invoke(prompt)

    leads: list[VendorLead] = []
    for call in response.tool_calls:
        if call["name"] == "record_vendor_leads":
            for item in call["args"].get("leads", []):
                leads.append(
                    VendorLead(
                        category=category.label,
                        name=item.get("name", "Unknown"),
                        price_estimate=item.get("price_estimate", "N/A"),
                        location=item.get("location", city),
                        contact_or_source=item.get("contact_or_source", ""),
                        notes=item.get("notes", ""),
                    )
                )

    summary_prompt = f"""In 2-3 sentences, summarize the pricing landscape for
{category.label} in {city} based on these leads, and call out the single
best budget-friendly pick:

{json.dumps(leads, indent=2)}
"""
    summary = _llm.invoke(summary_prompt).content

    return leads, f"### {category.label}\n{summary}"


def write_final_report(city: str, category_summaries: list[str], leads: list[VendorLead]) -> str:
    """Supervisor node: synthesize all specialist outputs into one report."""
    prompt = f"""You are the supervisor agent coordinating a home-services vendor
search in {city}. Each specialist has reported back below. Write a final,
well-organized markdown report for the homeowner:

1. A short overview (2-3 sentences).
2. One section per category with a compact markdown table of leads
   (Vendor | Price | Location | Source | Notes), sorted cheapest-first
   where prices are comparable.
3. A closing "Overall budget tips" section with 2-3 practical tips for
   negotiating/bundling this work in India.

SPECIALIST SUMMARIES:
{chr(10).join(category_summaries)}

RAW LEADS (JSON):
{json.dumps(leads, indent=2)}
"""
    return _llm.invoke(prompt).content
