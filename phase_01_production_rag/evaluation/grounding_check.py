# Grounding Check Implementation
"""
Grounding check: verifies that a generated answer is supported by the retrieved context.
Uses sentence-level overlap and an optional LLM-based entailment check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class GroundingResult:
    is_grounded: bool
    score: float                        # 0.0 – 1.0
    ungrounded_claims: list[str] = field(default_factory=list)
    grounded_claims: list[str] = field(default_factory=list)
    method: str = "lexical"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sentences(text: str) -> list[str]:
    """Split text into non-empty sentences."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _token_overlap(claim: str, context: str) -> float:
    """Jaccard token overlap between a claim and a context window."""
    claim_tokens = set(_normalize(claim).split())
    ctx_tokens = set(_normalize(context).split())
    if not claim_tokens:
        return 0.0
    intersection = claim_tokens & ctx_tokens
    union = claim_tokens | ctx_tokens
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# Core grounding checker
# ---------------------------------------------------------------------------

class GroundingChecker:
    """
    Checks whether each sentence in `answer` is supported by `context`.

    Parameters
    ----------
    threshold : float
        Minimum token-overlap score to consider a claim grounded (default 0.25).
    grounded_ratio : float
        Fraction of claims that must be grounded for the answer to pass (default 0.8).
    """

    def __init__(self, threshold: float = 0.25, grounded_ratio: float = 0.8):
        self.threshold = threshold
        self.grounded_ratio = grounded_ratio

    def check(self, answer: str, context: str) -> GroundingResult:
        """Return a GroundingResult for the given answer / context pair."""
        claims = _sentences(answer)
        if not claims:
            return GroundingResult(is_grounded=True, score=1.0, method="lexical")

        grounded: list[str] = []
        ungrounded: list[str] = []

        for claim in claims:
            score = _token_overlap(claim, context)
            if score >= self.threshold:
                grounded.append(claim)
            else:
                ungrounded.append(claim)

        ratio = len(grounded) / len(claims)
        return GroundingResult(
            is_grounded=ratio >= self.grounded_ratio,
            score=round(ratio, 4),
            grounded_claims=grounded,
            ungrounded_claims=ungrounded,
            method="lexical",
        )

    def check_batch(
        self, answers: list[str], contexts: list[str]
    ) -> list[GroundingResult]:
        """Check multiple answer/context pairs."""
        if len(answers) != len(contexts):
            raise ValueError("answers and contexts must have the same length")
        return [self.check(a, c) for a, c in zip(answers, contexts)]


# ---------------------------------------------------------------------------
# Optional LLM-based grounding (requires anthropic package)
# ---------------------------------------------------------------------------

class LLMGroundingChecker:
    """
    Uses Claude to judge whether an answer is supported by the context.
    Falls back gracefully if the anthropic package is not installed.
    """

    PROMPT = (
        "You are a grounding evaluator. Given a CONTEXT and an ANSWER, "
        "determine whether every factual claim in the ANSWER is directly supported by the CONTEXT.\n\n"
        "CONTEXT:\n{context}\n\n"
        "ANSWER:\n{answer}\n\n"
        "Reply with a JSON object with keys:\n"
        "  'is_grounded' (bool),\n"
        "  'score' (float 0-1),\n"
        "  'ungrounded_claims' (list of strings).\n"
        "Return only valid JSON, no extra text."
    )

    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        self.model = model
        self._client: Optional[object] = None
        try:
            import anthropic  # noqa: PLC0415
            self._client = anthropic.Anthropic()
        except ImportError:
            pass

    def check(self, answer: str, context: str) -> GroundingResult:
        if self._client is None:
            raise RuntimeError(
                "anthropic package not installed. "
                "Run `pip install anthropic` or use GroundingChecker instead."
            )

        import json  # noqa: PLC0415

        message = self._client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": self.PROMPT.format(context=context, answer=answer),
                }
            ],
        )
        raw = message.content[0].text
        data = json.loads(raw)
        return GroundingResult(
            is_grounded=bool(data.get("is_grounded", False)),
            score=float(data.get("score", 0.0)),
            ungrounded_claims=data.get("ungrounded_claims", []),
            method="llm",
        )


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    context = (
        "The Eiffel Tower is located in Paris, France. "
        "It was constructed between 1887 and 1889 as the entrance arch for the 1889 World's Fair."
    )
    answer_good = (
        "The Eiffel Tower is in Paris. It was built for the 1889 World's Fair."
    )
    answer_bad = (
        "The Eiffel Tower is in Berlin. It was built in 1950 by German engineers."
    )

    checker = GroundingChecker()

    for label, ans in [("GROUNDED", answer_good), ("HALLUCINATED", answer_bad)]:
        result = checker.check(ans, context)
        print(f"\n[{label}]")
        print(f"  is_grounded : {result.is_grounded}")
        print(f"  score       : {result.score}")
        print(f"  ungrounded  : {result.ungrounded_claims}")
