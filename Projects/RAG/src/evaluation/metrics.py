"""
RAG Evaluation Metrics
Comprehensive metrics for evaluating retrieval and generation quality
"""

from typing import List, Dict, Any, Set
from loguru import logger
import numpy as np


class RAGEvaluator:
    """
    Evaluator for RAG system performance
    Includes retrieval and generation metrics
    """
    
    def __init__(self):
        logger.info("RAGEvaluator initialized")
    
    def evaluate_retrieval(
        self,
        retrieved_docs: List[str],
        relevant_docs: List[str],
        k_values: List[int] = [1, 3, 5, 10]
    ) -> Dict[str, Any]:
        """
        Evaluate retrieval performance
        
        Args:
            retrieved_docs: List of retrieved document IDs (in rank order)
            relevant_docs: List of relevant document IDs (ground truth)
            k_values: K values for precision@k and recall@k
            
        Returns:
            Dictionary of metrics
        """
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)
        
        metrics = {}
        
        # Precision, Recall, F1 for different K values
        for k in k_values:
            retrieved_at_k = set(retrieved_docs[:k])
            
            precision = self.precision_at_k(retrieved_at_k, relevant_set)
            recall = self.recall_at_k(retrieved_at_k, relevant_set)
            f1 = self.f1_score(precision, recall)
            
            metrics[f"precision@{k}"] = precision
            metrics[f"recall@{k}"] = recall
            metrics[f"f1@{k}"] = f1
        
        # Mean Reciprocal Rank (MRR)
        metrics["mrr"] = self.mean_reciprocal_rank(retrieved_docs, relevant_set)
        
        # Normalized Discounted Cumulative Gain (NDCG)
        # Create relevance scores (1 for relevant, 0 for not)
        relevance_scores = [
            1 if doc_id in relevant_set else 0 
            for doc_id in retrieved_docs
        ]
        metrics["ndcg@10"] = self.ndcg_at_k(relevance_scores, k=10)
        
        logger.debug(f"Retrieval evaluation completed: {metrics}")
        return metrics
    
    def precision_at_k(
        self,
        retrieved: Set[str],
        relevant: Set[str]
    ) -> float:
        """
        Calculate Precision@K
        
        Precision = |Retrieved ∩ Relevant| / |Retrieved|
        
        Args:
            retrieved: Set of retrieved document IDs
            relevant: Set of relevant document IDs
            
        Returns:
            Precision score
        """
        if not retrieved:
            return 0.0
        
        intersection = retrieved & relevant
        return len(intersection) / len(retrieved)
    
    def recall_at_k(
        self,
        retrieved: Set[str],
        relevant: Set[str]
    ) -> float:
        """
        Calculate Recall@K
        
        Recall = |Retrieved ∩ Relevant| / |Relevant|
        
        Args:
            retrieved: Set of retrieved document IDs
            relevant: Set of relevant document IDs
            
        Returns:
            Recall score
        """
        if not relevant:
            return 0.0
        
        intersection = retrieved & relevant
        return len(intersection) / len(relevant)
    
    def f1_score(self, precision: float, recall: float) -> float:
        """
        Calculate F1 score
        
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        
        Args:
            precision: Precision score
            recall: Recall score
            
        Returns:
            F1 score
        """
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def mean_reciprocal_rank(
        self,
        retrieved: List[str],
        relevant: Set[str]
    ) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR)
        
        MRR = 1 / rank of first relevant document
        
        Args:
            retrieved: List of retrieved document IDs (ordered)
            relevant: Set of relevant document IDs
            
        Returns:
            MRR score
        """
        for rank, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                return 1.0 / rank
        
        return 0.0
    
    def ndcg_at_k(
        self,
        relevance_scores: List[float],
        k: int = 10
    ) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG)
        
        DCG = Σ (2^rel_i - 1) / log2(i + 1)
        NDCG = DCG / IDCG (ideal DCG)
        
        Args:
            relevance_scores: List of relevance scores (in rank order)
            k: Cutoff for evaluation
            
        Returns:
            NDCG score
        """
        def dcg_at_k(scores, k):
            scores = scores[:k]
            if not scores:
                return 0.0
            
            dcg = 0.0
            for i, score in enumerate(scores, 1):
                dcg += (2 ** score - 1) / np.log2(i + 1)
            
            return dcg
        
        # Calculate DCG
        dcg = dcg_at_k(relevance_scores, k)
        
        # Calculate IDCG (ideal DCG with perfect ranking)
        ideal_scores = sorted(relevance_scores, reverse=True)
        idcg = dcg_at_k(ideal_scores, k)
        
        if idcg == 0:
            return 0.0
        
        return dcg / idcg
    
    def evaluate_answer_quality(
        self,
        generated_answer: str,
        context_docs: List[str],
        reference_answer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate answer quality
        
        Args:
            generated_answer: Generated answer
            context_docs: Context documents used
            reference_answer: Optional reference answer for comparison
            
        Returns:
            Dictionary of quality metrics
        """
        metrics = {}
        
        # Answer length
        metrics["answer_length"] = len(generated_answer.split())
        
        # Check if answer acknowledges uncertainty
        uncertainty_phrases = [
            "i don't know",
            "i cannot answer",
            "not enough information",
            "unclear",
            "i'm not sure"
        ]
        metrics["acknowledges_uncertainty"] = any(
            phrase in generated_answer.lower() 
            for phrase in uncertainty_phrases
        )
        
        # Context grounding (simple check)
        # More sophisticated methods would use NLI models
        metrics["context_overlap"] = self._calculate_context_overlap(
            generated_answer, context_docs
        )
        
        # If reference answer provided, calculate similarity
        if reference_answer:
            metrics["reference_similarity"] = self._calculate_text_similarity(
                generated_answer, reference_answer
            )
        
        return metrics
    
    def _calculate_context_overlap(
        self,
        answer: str,
        contexts: List[str]
    ) -> float:
        """
        Calculate overlap between answer and context
        
        Args:
            answer: Generated answer
            contexts: Context documents
            
        Returns:
            Overlap ratio
        """
        answer_words = set(answer.lower().split())
        context_words = set()
        
        for context in contexts:
            context_words.update(context.lower().split())
        
        if not answer_words:
            return 0.0
        
        overlap = answer_words & context_words
        return len(overlap) / len(answer_words)
    
    def _calculate_text_similarity(
        self,
        text1: str,
        text2: str
    ) -> float:
        """
        Calculate similarity between two texts (simple word overlap)
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)  # Jaccard similarity
    
    def batch_evaluate(
        self,
        queries: List[str],
        retrieved_results: List[List[str]],
        relevant_results: List[List[str]],
        generated_answers: Optional[List[str]] = None,
        reference_answers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate multiple queries in batch
        
        Args:
            queries: List of queries
            retrieved_results: List of retrieved doc IDs for each query
            relevant_results: List of relevant doc IDs for each query
            generated_answers: Optional list of generated answers
            reference_answers: Optional list of reference answers
            
        Returns:
            Aggregated metrics
        """
        retrieval_metrics = []
        
        for retrieved, relevant in zip(retrieved_results, relevant_results):
            metrics = self.evaluate_retrieval(retrieved, relevant)
            retrieval_metrics.append(metrics)
        
        # Aggregate retrieval metrics
        aggregated = self._aggregate_metrics(retrieval_metrics)
        
        # Evaluate answers if provided
        if generated_answers:
            answer_metrics = []
            for i, answer in enumerate(generated_answers):
                context = retrieved_results[i] if i < len(retrieved_results) else []
                ref = reference_answers[i] if reference_answers and i < len(reference_answers) else None
                
                # For this evaluation, we'll use the retrieved strings as context
                # In practice, you'd retrieve the actual document content
                metrics = self.evaluate_answer_quality(answer, context, ref)
                answer_metrics.append(metrics)
            
            aggregated["answer_quality"] = self._aggregate_metrics(answer_metrics)
        
        logger.info("Batch evaluation completed")
        return aggregated
    
    def _aggregate_metrics(
        self,
        metrics_list: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Aggregate metrics across multiple evaluations
        
        Args:
            metrics_list: List of metric dictionaries
            
        Returns:
            Aggregated metrics (mean, min, max)
        """
        if not metrics_list:
            return {}
        
        # Get all metric names
        all_keys = set()
        for metrics in metrics_list:
            all_keys.update(metrics.keys())
        
        aggregated = {}
        
        for key in all_keys:
            values = [
                m[key] for m in metrics_list 
                if key in m and isinstance(m[key], (int, float))
            ]
            
            if values:
                aggregated[f"{key}_mean"] = np.mean(values)
                aggregated[f"{key}_std"] = np.std(values)
                aggregated[f"{key}_min"] = np.min(values)
                aggregated[f"{key}_max"] = np.max(values)
        
        return aggregated


if __name__ == "__main__":
    # Test the evaluator
    evaluator = RAGEvaluator()
    
    # Test retrieval evaluation
    retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    relevant = ["doc1", "doc3", "doc6"]
    
    metrics = evaluator.evaluate_retrieval(retrieved, relevant)
    
    print("Retrieval Metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
