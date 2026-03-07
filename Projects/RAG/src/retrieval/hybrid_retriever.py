"""
Hybrid Retriever
Combines vector and BM25 retrieval with fusion strategies
"""

from typing import List, Dict, Optional, Any
from loguru import logger
import numpy as np

from .vector_retriever import VectorRetriever
from .bm25_retriever import BM25Retriever


class HybridRetriever:
    """
    Hybrid retrieval combining vector and BM25 search
    Uses Reciprocal Rank Fusion (RRF) or weighted combination
    """
    
    def __init__(
        self,
        vector_retriever: VectorRetriever,
        bm25_retriever: BM25Retriever,
        fusion_method: str = "rrf",
        alpha: float = 0.5,
        rrf_k: int = 60,
        top_k: int = 10
    ):
        """
        Initialize hybrid retriever
        
        Args:
            vector_retriever: Vector retriever instance
            bm25_retriever: BM25 retriever instance
            fusion_method: Fusion method ('rrf' or 'weighted')
            alpha: Weight for vector search (0-1) in weighted fusion
            rrf_k: Constant for RRF (typically 60)
            top_k: Number of final results to return
        """
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.fusion_method = fusion_method
        self.alpha = alpha
        self.rrf_k = rrf_k
        self.top_k = top_k
        
        if fusion_method not in ["rrf", "weighted"]:
            raise ValueError("fusion_method must be 'rrf' or 'weighted'")
        
        if not 0 <= alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")
        
        logger.info(
            f"HybridRetriever initialized with "
            f"fusion={fusion_method}, alpha={alpha}, rrf_k={rrf_k}"
        )
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents using hybrid search
        
        Args:
            query: Search query
            top_k: Number of results (overrides default)
            
        Returns:
            List of retrieved documents with fused scores
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
        
        k = top_k or self.top_k
        
        # Retrieve from both sources
        # Retrieve more than needed for better fusion
        retrieval_k = k * 2
        
        vector_results = self.vector_retriever.retrieve(query, top_k=retrieval_k)
        bm25_results = self.bm25_retriever.retrieve(query, top_k=retrieval_k)
        
        logger.debug(
            f"Retrieved {len(vector_results)} vector results, "
            f"{len(bm25_results)} BM25 results"
        )
        
        # Fuse results
        if self.fusion_method == "rrf":
            fused_results = self._reciprocal_rank_fusion(
                vector_results, bm25_results
            )
        else:  # weighted
            fused_results = self._weighted_fusion(
                vector_results, bm25_results
            )
        
        # Return top-k
        final_results = fused_results[:k]
        
        logger.info(f"Retrieved {len(final_results)} documents via hybrid search")
        return final_results
    
    def _reciprocal_rank_fusion(
        self,
        vector_results: List[Dict],
        bm25_results: List[Dict]
    ) -> List[Dict]:
        """
        Fuse results using Reciprocal Rank Fusion (RRF)
        
        RRF Formula: score(d) = Σ 1 / (k + rank(d))
        
        Args:
            vector_results: Results from vector search
            bm25_results: Results from BM25 search
            
        Returns:
            Fused and sorted results
        """
        # Build document scores
        doc_scores = {}
        doc_data = {}
        
        # Add vector results
        for doc in vector_results:
            doc_id = doc["id"]
            rank = doc["rank"]
            rrf_score = 1.0 / (self.rrf_k + rank)
            
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + rrf_score
            doc_data[doc_id] = doc
        
        # Add BM25 results
        for doc in bm25_results:
            doc_id = doc["id"]
            rank = doc["rank"]
            rrf_score = 1.0 / (self.rrf_k + rank)
            
            doc_scores[doc_id] = doc_scores.get(doc_id, 0) + rrf_score
            
            # Store doc data if not already present
            if doc_id not in doc_data:
                doc_data[doc_id] = doc
        
        # Sort by fused score
        sorted_doc_ids = sorted(
            doc_scores.keys(),
            key=lambda x: doc_scores[x],
            reverse=True
        )
        
        # Build final results
        fused_results = []
        for rank, doc_id in enumerate(sorted_doc_ids):
            doc = doc_data[doc_id].copy()
            doc["score"] = doc_scores[doc_id]
            doc["rank"] = rank + 1
            doc["retrieval_method"] = "hybrid_rrf"
            fused_results.append(doc)
        
        return fused_results
    
    def _weighted_fusion(
        self,
        vector_results: List[Dict],
        bm25_results: List[Dict]
    ) -> List[Dict]:
        """
        Fuse results using weighted score combination
        
        Score = alpha * normalized_vector_score + (1-alpha) * normalized_bm25_score
        
        Args:
            vector_results: Results from vector search
            bm25_results: Results from BM25 search
            
        Returns:
            Fused and sorted results
        """
        # Normalize scores
        vector_scores = self._normalize_scores(
            {doc["id"]: doc["score"] for doc in vector_results}
        )
        bm25_scores = self._normalize_scores(
            {doc["id"]: doc["score"] for doc in bm25_results}
        )
        
        # Combine scores
        doc_scores = {}
        doc_data = {}
        
        # Get all document IDs
        all_doc_ids = set(vector_scores.keys()) | set(bm25_scores.keys())
        
        for doc_id in all_doc_ids:
            vector_score = vector_scores.get(doc_id, 0.0)
            bm25_score = bm25_scores.get(doc_id, 0.0)
            
            # Weighted combination
            combined_score = (
                self.alpha * vector_score +
                (1 - self.alpha) * bm25_score
            )
            
            doc_scores[doc_id] = combined_score
            
            # Store doc data
            for results in [vector_results, bm25_results]:
                for doc in results:
                    if doc["id"] == doc_id and doc_id not in doc_data:
                        doc_data[doc_id] = doc
                        break
        
        # Sort by fused score
        sorted_doc_ids = sorted(
            doc_scores.keys(),
            key=lambda x: doc_scores[x],
            reverse=True
        )
        
        # Build final results
        fused_results = []
        for rank, doc_id in enumerate(sorted_doc_ids):
            doc = doc_data[doc_id].copy()
            doc["score"] = doc_scores[doc_id]
            doc["rank"] = rank + 1
            doc["retrieval_method"] = "hybrid_weighted"
            fused_results.append(doc)
        
        return fused_results
    
    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize scores to [0, 1] range using min-max normalization
        
        Args:
            scores: Dictionary of doc_id -> score
            
        Returns:
            Normalized scores
        """
        if not scores:
            return {}
        
        score_values = list(scores.values())
        min_score = min(score_values)
        max_score = max(score_values)
        
        # Avoid division by zero
        if max_score == min_score:
            return {doc_id: 1.0 for doc_id in scores}
        
        normalized = {
            doc_id: (score - min_score) / (max_score - min_score)
            for doc_id, score in scores.items()
        }
        
        return normalized


if __name__ == "__main__":
    print("HybridRetriever module ready")
