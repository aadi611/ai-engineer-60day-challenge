# Hallucination Detection Implementation
"""
Hallucination detection for RAG pipelines.

Two complementary approaches:
  1. LexicalHallucinationDetector  — fast, no API calls, token/n-gram overlap
  2. LLMHallucinationDetector      — LLM judge via Claude (requires anthropic)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class HallucinationResult:
    has_hallucination: bool
    confidence: float               # 0.0 = clean, 1.0 = definitely hallucinated
    hallucinated_spans: list[str] = field(default_factory=list)
    supported_spans: list[str] = field(default_factory=list)
    method: str = "lexical"

    @property
    def summary(self) -> str:
        status = "HALLUCINATED" if self.has_hallucination else "GROUNDED"
        return f"[{status}] confidence={self.confidence:.2f} | flagged={len(self.hallucinated_spans)}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _ngrams(text: str, n: int) -> set[str]:
    tokens = re.sub(r"\s+", " ", text.lower().strip()).split()
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _containment(claim: str, context: str, n: int = 3) -> float:
    """Fraction of claim n-grams that appear in context."""
    claim_grams = _ngrams(claim, n)
    if not claim_grams:
        # fall back to unigram overlap for very short claims
        claim_grams = _ngrams(claim, 1)
    if not claim_grams:
        return 1.0  # empty claim — treat as supported
    ctx_grams = _ngrams(context, n) if n > 1 else _ngrams(context, 1)
    return len(claim_grams & ctx_grams) / len(claim_grams)


# ---------------------------------------------------------------------------
# Lexical detector
# ---------------------------------------------------------------------------

class LexicalHallucinationDetector:
    """
    Flags sentences whose n-gram containment in the context falls below a threshold.

    Parameters
    ----------
    ngram_size : int
        Size of n-grams used for overlap (default 3 — trigrams).
    threshold : float
        Minimum containment score to consider a sentence supported (default 0.3).
    hallucination_ratio : float
        Fraction of unsupported sentences that triggers has_hallucination=True (default 0.3).
    """

    def __init__(
        self,
        ngram_size: int = 3,
        threshold: float = 0.3,
        hallucination_ratio: float = 0.3,
    ):
        self.ngram_size = ngram_size
        self.threshold = threshold
        self.hallucination_ratio = hallucination_ratio

    def detect(self, answer: str, context: str) -> HallucinationResult:
        sentences = _sentences(answer)
        if not sentences:
            return HallucinationResult(has_hallucination=False, confidence=0.0)

        hallucinated: list[str] = []
        supported: list[str] = []

        for sent in sentences:
            score = _containment(sent, context, self.ngram_size)
            if score < self.threshold:
                hallucinated.append(sent)
            else:
                supported.append(sent)

        h_ratio = len(hallucinated) / len(sentences)
        confidence = round(h_ratio, 4)

        return HallucinationResult(
            has_hallucination=h_ratio >= self.hallucination_ratio,
            confidence=confidence,
            hallucinated_spans=hallucinated,
            supported_spans=supported,
            method="lexical-ngram",
        )

    def detect_batch(
        self, answers: list[str], contexts: list[str]
    ) -> list[HallucinationResult]:
        if len(answers) != len(contexts):
            raise ValueError("answers and contexts must have the same length")
        return [self.detect(a, c) for a, c in zip(answers, contexts)]


# ---------------------------------------------------------------------------
# Numeric claim checker (catches fabricated numbers / dates)
# ---------------------------------------------------------------------------

def _extract_numbers(text: str) -> set[str]:
    return set(re.findall(r"\b\d[\d,./]*\b", text))


def check_numeric_consistency(answer: str, context: str) -> dict:
    """
    Returns a dict with fabricated numbers not present in context.
    Useful as a lightweight standalone check or combined with other detectors.
    """
    answer_nums = _extract_numbers(answer)
    context_nums = _extract_numbers(context)
    fabricated = answer_nums - context_nums
    return {
        "fabricated_numbers": sorted(fabricated),
        "answer_numbers": sorted(answer_nums),
        "context_numbers": sorted(context_nums),
        "has_numeric_hallucination": bool(fabricated),
    }


# ---------------------------------------------------------------------------
# LLM-based detector (Claude)
# ---------------------------------------------------------------------------

class LLMHallucinationDetector:
    """
    Uses Claude as a judge to detect hallucinations.
    Requires `pip install anthropic`.
    """

    PROMPT = (
        "You are a hallucination detector for RAG systems.\n\n"
        "CONTEXT (retrieved documents — treat as ground truth):\n{context}\n\n"
        "GENERATED ANSWER:\n{answer}\n\n"
        "Task: identify every claim in the ANSWER that is NOT supported by the CONTEXT "
        "(i.e., fabricated, contradicted, or unverifiable).\n\n"
        "Respond with a JSON object:\n"
        "{{\n"
        "  \"has_hallucination\": <bool>,\n"
        "  \"confidence\": <float 0-1, where 1 = certain hallucination>,\n"
        "  \"hallucinated_spans\": [<strings>],\n"
        "  \"supported_spans\": [<strings>],\n"
        "  \"reasoning\": \"<one sentence>\"\n"
        "}}\n"
        "Return only valid JSON."
    )

    def __init__(self, model: str = "claude-haiku-4-5-20251001"):
        self.model = model
        self._client: Optional[object] = None
        try:
            import anthropic  # noqa: PLC0415
            self._client = anthropic.Anthropic()
        except ImportError:
            pass

    def detect(self, answer: str, context: str) -> HallucinationResult:
        if self._client is None:
            raise RuntimeError(
                "anthropic package not installed. "
                "Run `pip install anthropic` or use LexicalHallucinationDetector."
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
        return HallucinationResult(
            has_hallucination=bool(data.get("has_hallucination", False)),
            confidence=float(data.get("confidence", 0.0)),
            hallucinated_spans=data.get("hallucinated_spans", []),
            supported_spans=data.get("supported_spans", []),
            method="llm",
        )


# ---------------------------------------------------------------------------
# Combined pipeline
# ---------------------------------------------------------------------------

class HallucinationPipeline:
    """
    Runs lexical + numeric checks together and returns an aggregated result.
    Optionally escalates to LLM when the lexical score is uncertain.
    """

    def __init__(
        self,
        lexical: Optional[LexicalHallucinationDetector] = None,
        llm: Optional[LLMHallucinationDetector] = None,
        llm_escalation_threshold: float = 0.2,
    ):
        self.lexical = lexical or LexicalHallucinationDetector()
        self.llm = llm
        self.llm_escalation_threshold = llm_escalation_threshold

    def run(self, answer: str, context: str) -> HallucinationResult:
        lex_result = self.lexical.detect(answer, context)
        numeric = check_numeric_consistency(answer, context)

        # Escalate to LLM if available and result is borderline or positive
        if self.llm and lex_result.confidence >= self.llm_escalation_threshold:
            try:
                return self.llm.detect(answer, context)
            except Exception:
                pass  # fall through to lexical result on API failure

        # Incorporate numeric check into lexical result
        if numeric["has_numeric_hallucination"]:
            lex_result.has_hallucination = True
            lex_result.hallucinated_spans.extend(
                [f"[number] {n}" for n in numeric["fabricated_numbers"]]
            )

        return lex_result


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    context = (
        "The Eiffel Tower is located in Paris, France. "
        "It was constructed between 1887 and 1889 and stands 330 metres tall."
    )
    answers = {
        "clean":       "The Eiffel Tower is in Paris and is 330 metres tall.",
        "hallucinated": "The Eiffel Tower is in Berlin and stands 500 metres tall. It was built in 1950.",
        "partial":     "The Eiffel Tower is in Paris. It was designed by Leonardo da Vinci.",
    }

    detector = LexicalHallucinationDetector()
    pipeline = HallucinationPipeline(lexical=detector)

    for label, ans in answers.items():
        result = pipeline.run(ans, context)
        print(f"\n[{label.upper()}]")
        print(f"  {result.summary}")
        if result.hallucinated_spans:
            for span in result.hallucinated_spans:
                print(f"    - {span}")
