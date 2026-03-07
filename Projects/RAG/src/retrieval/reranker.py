"""
Reranker
Cross-encoder based reranking for improved relevance
"""

from typing import List, Dict, Any, Optional
from loguru import logger
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class Reranker:
    """
    Cross-encoder reranker for relevance scoring
    Provides more accurate relevance scores than bi-encoders
    """
    
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_k: int = 5,
        batch_size: int = 32,
        device: Optional[str] = None
    ):
        """
        Initialize reranker
        
        Args:
            model_name: HuggingFace model name
            top_k: Number of top results to return after reranking
            batch_size: Batch size for processing
            device: Device for model ('cuda',  'cpu', or None for auto)
        """
        self.model_name = model_name
        self.top_k = top_k
        self.batch_size = batch_size
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        # Load model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Reranker loaded: {model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading reranker model: {e}")
            raise
    
    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents based on query relevance
        
        Args:
            query: Search query
            documents: List of retrieved documents
            top_k: Number of top results (overrides default)
            
        Returns:
            Reranked documents with updated scores
        """
        if not documents:
            logger.warning("No documents to rerank")
            return []
        
        k = top_k or self.top_k
        
        # Prepare query-document pairs
        pairs = []
        for doc in documents:
            pairs.append([query, doc["content"]])
        
        # Score in batches
        scores = []
        with torch.no_grad():
            for i in range(0, len(pairs), self.batch_size):
                batch_pairs = pairs[i:i + self.batch_size]
                batch_scores = self._score_batch(batch_pairs)
                scores.extend(batch_scores)
        
        # Update documents with reranked scores
        reranked_docs = []
        for doc, score in zip(documents, scores):
            reranked_doc = doc.copy()
            reranked_doc["rerank_score"] = score
            reranked_doc["original_score"] = doc.get("score", 0.0)
            reranked_docs.append(reranked_doc)
        
        # Sort by rerank score
        reranked_docs.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Update ranks
        for rank, doc in enumerate(reranked_docs):
            doc["rank"] = rank + 1
            doc["retrieval_method"] = doc.get("retrieval_method", "unknown") + "_reranked"
        
        # Return top-k
        final_results = reranked_docs[:k]
        
        logger.info(f"Reranked {len(documents)} documents, returning top {len(final_results)}")
        return final_results
    
    def _score_batch(self, pairs: List[List[str]]) -> List[float]:
        """
        Score a batch of query-document pairs
        
        Args:
            pairs: List of [query, document] pairs
            
        Returns:
            List of relevance scores
        """
        # Tokenize
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        # Get scores
        outputs = self.model(**inputs)
        logits = outputs.logits
        
        # Convert to scores
        scores = torch.sigmoid(logits).squeeze(-1).cpu().tolist()
        
        # Handle single item case
        if not isinstance(scores, list):
            scores = [scores]
        
        return scores


if __name__ == "__main__":
    # Test reranker
    print("Reranker module ready")
    print("Note: First run will download the model")
    
    try:
        reranker = Reranker(top_k=3)
        
        query = "machine learning"
        docs = [
            {"id": "1", "content": "Deep learning is a subset of machine learning", "score": 0.8},
            {"id": "2", "content": "The weather today is sunny", "score": 0.7},
            {"id": "3", "content": "Machine learning algorithms learn from data", "score": 0.9}
        ]
        
        reranked = reranker.rerank(query, docs)
        print(f"\nReranked {len(reranked)} documents:")
        for doc in reranked:
            print(f"  Rank {doc['rank']}: {doc['id']} - Score: {doc['rerank_score']:.4f}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have transformers and torch installed")
