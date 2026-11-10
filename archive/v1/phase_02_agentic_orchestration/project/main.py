"""CLI for the Home Services Vendor Finder multi-agent system.

Usage:
    python main.py --city "Bengaluru" --categories wall_revamp,plumber,carpenter
    python main.py --city "Pune" --categories "wpc panels" --budget "under 15000 total"
"""

from __future__ import annotations
import argparse
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import time

load_dotenv()

from categories import CATEGORIES  # noqa: E402  (after load_dotenv)
from graph import build_graph  # noqa: E402

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Home Services Vendor Finder (multi-agent)")
    parser.add_argument("--city", required=True, help="City in India, e.g. 'Bengaluru'")
    parser.add_argument(
        "--categories",
        required=True,
        help=f"Comma-separated categories. Available: {', '.join(CATEGORIES)}",
    )
    parser.add_argument("--budget", default="", help="Optional budget note, e.g. 'under 20000 total'")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    categories = [c.strip() for c in args.categories.split(",") if c.strip()]

    console.print(f"[bold cyan]Searching {len(categories)} categories in {args.city}...[/bold cyan]")

    graph = build_graph()
    result = graph.invoke(
        {
            "city": args.city,
            "categories": categories,
            "budget_note": args.budget,
            "leads": [],
            "category_summaries": [],
            "final_report": "",
        }
    )

    console.print(Markdown(result["final_report"]))


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
