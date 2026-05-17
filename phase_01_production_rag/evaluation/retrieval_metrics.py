# Retrieval Metrics Implementation
"""
Standard retrieval evaluation metrics for RAG pipelines.

Metrics implemented:
  - Precision@K, Recall@K, F1@K
  - Average Precision (AP) / Mean Average Precision (MAP)
  - NDCG@K  (Normalized Discounted Cumulative Gain)
  - MRR     (Mean Reciprocal Rank)
  - Hit Rate@K
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Union


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    f1_at_k: float
    average_precision: float
    ndcg_at_k: float
    reciprocal_rank: float
    hit_rate: bool
    k: int

    def __str__(self) -> str:
        return (
            f"Retrieval Metrics @{self.k}\n"
            f"  Precision : {self.precision_at_k:.4f}\n"
            f"  Recall    : {self.recall_at_k:.4f}\n"
            f"  F1        : {self.f1_at_k:.4f}\n"
            f"  AP        : {self.average_precision:.4f}\n"
            f"  NDCG      : {self.ndcg_at_k:.4f}\n"
            f"  RR        : {self.reciprocal_rank:.4f}\n"
            f"  Hit Rate  : {self.hit_rate}"
        )


@dataclass
class AggregateMetrics:
    map_at_k: float
    mean_ndcg_at_k: float
    mrr: float
    mean_hit_rate: float
    mean_precision_at_k: float
    mean_recall_at_k: float
    mean_f1_at_k: float
    k: int
    num_queries: int

    def __str__(self) -> str:
        return (
            f"Aggregate Metrics @{self.k}  (n={self.num_queries})\n"
            f"  MAP       : {self.map_at_k:.4f}\n"
            f"  Mean NDCG : {self.mean_ndcg_at_k:.4f}\n"
            f"  MRR       : {self.mrr:.4f}\n"
            f"  Hit Rate  : {self.mean_hit_rate:.4f}\n"
            f"  Precision : {self.mean_precision_at_k:.4f}\n"
            f"  Recall    : {self.mean_recall_at_k:.4f}\n"
            f"  F1        : {self.mean_f1_at_k:.4f}"
        )


# ---------------------------------------------------------------------------
# Per-query metrics
# ---------------------------------------------------------------------------

def precision_at_k(retrieved: list, relevant: set, k: int) -> float:
    """Fraction of top-K retrieved docs that are relevant."""
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / k if k > 0 else 0.0


def recall_at_k(retrieved: list, relevant: set, k: int) -> float:
    """Fraction of relevant docs found in top-K."""
    if not relevant:
        return 0.0
    top_k = retrieved[:k]
    hits = sum(1 for doc in top_k if doc in relevant)
    return hits / len(relevant)


def f1_at_k(retrieved: list, relevant: set, k: int) -> float:
    p = precision_at_k(retrieved, relevant, k)
    r = recall_at_k(retrieved, relevant, k)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def average_precision(retrieved: list, relevant: set, k: int) -> float:
    """
    Average Precision: mean of precision values at each rank where a relevant
    doc is retrieved, up to rank K.
    """
    if not relevant:
        return 0.0
    hits = 0
    score = 0.0
    for rank, doc in enumerate(retrieved[:k], start=1):
        if doc in relevant:
            hits += 1
            score += hits / rank
    return score / min(len(relevant), k)


def ndcg_at_k(
    retrieved: list,
    relevant: Union[set, dict],
    k: int,
) -> float:
    """
    NDCG@K. `relevant` can be:
      - a set  → binary relevance (rel=1 if present)
      - a dict → graded relevance  {doc_id: grade}
    """
    def rel(doc) -> float:
        if isinstance(relevant, dict):
            return float(relevant.get(doc, 0))
        return 1.0 if doc in relevant else 0.0

    def dcg(docs: list, cutoff: int) -> float:
        return sum(
            rel(doc) / math.log2(rank + 1)
            for rank, doc in enumerate(docs[:cutoff], start=1)
        )

    actual_dcg = dcg(retrieved, k)

    # ideal: sort by relevance descending
    if isinstance(relevant, dict):
        ideal_docs = sorted(relevant.keys(), key=lambda d: relevant[d], reverse=True)
    else:
        ideal_docs = list(relevant)

    ideal_dcg = dcg(ideal_docs, k)
    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0


def reciprocal_rank(retrieved: list, relevant: set) -> float:
    """1 / rank of the first relevant document (0 if none found)."""
    for rank, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1.0 / rank
    return 0.0


def hit_rate_at_k(retrieved: list, relevant: set, k: int) -> bool:
    """True if at least one relevant document appears in the top-K results."""
    return any(doc in relevant for doc in retrieved[:k])


# ---------------------------------------------------------------------------
# Convenience: compute all metrics for a single query
# ---------------------------------------------------------------------------

def evaluate_query(
    retrieved: list,
    relevant: Union[set, dict],
    k: int = 5,
) -> RetrievalMetrics:
    """
    Compute all retrieval metrics for a single query.

    Parameters
    ----------
    retrieved : list
        Ordered list of retrieved document IDs (most relevant first).
    relevant : set | dict
        Ground-truth relevant documents. Use a dict for graded relevance.
    k : int
        Cutoff rank.
    """
    rel_set = set(relevant) if isinstance(relevant, set) else set(relevant.keys())

    return RetrievalMetrics(
        precision_at_k=precision_at_k(retrieved, rel_set, k),
        recall_at_k=recall_at_k(retrieved, rel_set, k),
        f1_at_k=f1_at_k(retrieved, rel_set, k),
        average_precision=average_precision(retrieved, rel_set, k),
        ndcg_at_k=ndcg_at_k(retrieved, relevant, k),
        reciprocal_rank=reciprocal_rank(retrieved, rel_set),
        hit_rate=hit_rate_at_k(retrieved, rel_set, k),
        k=k,
    )


# ---------------------------------------------------------------------------
# Aggregate over a dataset of queries
# ---------------------------------------------------------------------------

def evaluate_dataset(
    queries: list[dict],
    k: int = 5,
) -> AggregateMetrics:
    """
    Aggregate metrics across multiple queries.

    Parameters
    ----------
    queries : list of dicts, each with keys:
        'retrieved' : list of doc IDs (ranked)
        'relevant'  : set or dict of relevant doc IDs
    k : int
        Cutoff rank.

    Example
    -------
    queries = [
        {"retrieved": ["d1", "d2", "d3"], "relevant": {"d1", "d3"}},
        {"retrieved": ["d4", "d1", "d5"], "relevant": {"d4"}},
    ]
    agg = evaluate_dataset(queries, k=3)
    """
    results = [evaluate_query(q["retrieved"], q["relevant"], k) for q in queries]
    n = len(results)
    if n == 0:
        raise ValueError("queries list is empty")

    def mean(attr: str) -> float:
        return sum(getattr(r, attr) for r in results) / n

    return AggregateMetrics(
        map_at_k=mean("average_precision"),
        mean_ndcg_at_k=mean("ndcg_at_k"),
        mrr=mean("reciprocal_rank"),
        mean_hit_rate=sum(r.hit_rate for r in results) / n,
        mean_precision_at_k=mean("precision_at_k"),
        mean_recall_at_k=mean("recall_at_k"),
        mean_f1_at_k=mean("f1_at_k"),
        k=k,
        num_queries=n,
    )


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Simulated retrieval results
    sample_queries = [
        {
            "retrieved": ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"],
            "relevant":  {"doc_1", "doc_3", "doc_5"},
        },
        {
            "retrieved": ["doc_6", "doc_2", "doc_1", "doc_7", "doc_8"],
            "relevant":  {"doc_6"},
        },
        {
            "retrieved": ["doc_9", "doc_10", "doc_2", "doc_3", "doc_1"],
            "relevant":  {"doc_3", "doc_10"},
        },
    ]

    K = 5
    print("=== Per-query metrics ===")
    for i, q in enumerate(sample_queries):
        metrics = evaluate_query(q["retrieved"], q["relevant"], k=K)
        print(f"\nQuery {i + 1}:")
        print(metrics)

    print("\n=== Aggregate metrics ===")
    agg = evaluate_dataset(sample_queries, k=K)
    print(agg)
