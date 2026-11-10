"""Shared state passed between nodes in the LangGraph orchestration graph."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class VendorLead(TypedDict):
    category: str
    name: str
    price_estimate: str
    location: str
    contact_or_source: str
    notes: str


class JobState(TypedDict):
    city: str
    categories: list[str]
    budget_note: str
    leads: Annotated[list[VendorLead], operator.add]
    category_summaries: Annotated[list[str], operator.add]
    final_report: str
