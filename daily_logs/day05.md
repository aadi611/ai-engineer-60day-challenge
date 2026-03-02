# Day 5 - February 25, 2026

## Topics Covered
- Hybrid Search Architecture
- BM25 Algorithm Implementation
- Vector Search vs Keyword Search
- Reciprocal Rank Fusion (RRF)
- Weighted Score Combination
- Sparse and Dense Retrieval
- Search Result Fusion Strategies
- Performance Benchmarking

## What I Learned
- **Hybrid Search Fundamentals**: Combining the strengths of keyword and semantic search
  - Keyword search (BM25): Excellent for exact matches, names, IDs, technical terms
  - Vector search: Captures semantic meaning and context
  - Hybrid: Best of both worlds for production systems
- **BM25 Algorithm**: Understanding the classic keyword search algorithm
  - Term frequency (TF) with saturation
  - Inverse document frequency (IDF)
  - Document length normalization
  - Tuning parameters: k1 (term saturation) and b (length normalization)
- **Reciprocal Rank Fusion (RRF)**: Combining rankings from multiple retrievers
  - Simple, effective fusion algorithm
  - No need to normalize scores
  - Formula: RRF score = Σ(1 / (k + rank_i)) where k is typically 60
- **Weighted Combination**: Alternative fusion strategy
  - Normalize scores from both retrievers
  - Apply weights (e.g., 0.7 vector + 0.3 keyword)
  - Requires careful score normalization
- **When to Use What**:
  - Pure vector: Semantic queries, natural language
  - Pure keyword: Exact matches, IDs, technical jargon
  - Hybrid: Production systems needing both precision and recall
- **Performance Trade-offs**: 
  - Hybrid adds computational overhead
  - Significant improvement in recall and precision
  - Worth it for most production use cases

## Code/Projects
- Implemented BM25 search in `retrieval/bm25_search.py`
- Built hybrid search combining vector and BM25 in `retrieval/hybrid_search.py`
- Created RRF fusion algorithm
- Developed weighted score combination method
- Built benchmark comparison framework

## Challenges
- Tuning BM25 parameters (k1, b) for different document collections
- Choosing optimal weights for score combination
- Normalizing scores from different retrieval methods
- Deciding between RRF and weighted combination
- Balancing retrieval speed with result quality

## Resources
- BM25 Original Paper (Robertson & Zaragoza)
- "Reciprocal Rank Fusion" paper
- Elasticsearch BM25 Documentation
- Benchmarking hybrid search performance

## Tomorrow's Plan
- Implement RAG evaluation metrics (precision, recall, MRR, NDCG)
- Build ground truth test sets
- Create automated evaluation pipeline
- Measure and compare different retrieval strategies
