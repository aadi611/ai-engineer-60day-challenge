"""Home-services job categories and search hints used to steer each specialist agent."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    search_hints: list[str]


CATEGORIES: dict[str, Category] = {
    "wall_revamp": Category(
        key="wall_revamp",
        label="Wall Revamp / Texture Painting",
        search_hints=[
            "wall texture painting cost per sq ft India",
            "wall revamp contractors price list",
        ],
    ),
    "wpc_panels": Category(
        key="wpc_panels",
        label="WPC Wall Panels",
        search_hints=[
            "WPC panel installation cost per sq ft India",
            "WPC wall panel dealers price",
        ],
    ),
    "carpenter": Category(
        key="carpenter",
        label="Carpenter / Furniture Work",
        search_hints=[
            "carpenter charges per day India",
            "modular furniture carpenter rate list",
        ],
    ),
    "plumber": Category(
        key="plumber",
        label="Plumber",
        search_hints=[
            "plumber visiting charges India",
            "plumbing repair cost list",
        ],
    ),
    "electrician": Category(
        key="electrician",
        label="Electrician",
        search_hints=[
            "electrician charges per visit India",
            "electrical wiring cost per point",
        ],
    ),
    "painter": Category(
        key="painter",
        label="Painter (Wall/Interior)",
        search_hints=[
            "house painting cost per sq ft India",
            "painter contractor rate list",
        ],
    ),
}


def resolve_categories(requested: list[str]) -> list[Category]:
    """Map user-provided category keys/labels to known Category objects."""
    resolved = []
    for raw in requested:
        norm = raw.strip().lower().replace(" ", "_").replace("-", "_")
        if norm in CATEGORIES:
            resolved.append(CATEGORIES[norm])
            continue
        match = next(
            (c for c in CATEGORIES.values() if norm in c.label.lower()), None
        )
        if match:
            resolved.append(match)
        else:
            raise ValueError(
                f"Unknown category '{raw}'. Available: {', '.join(CATEGORIES)}"
            )
    return resolved
