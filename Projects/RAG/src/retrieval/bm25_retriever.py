"""
BM25 Retriever
Sparse keyword-based retrieval using BM25 algorithm
"""

from typing import List, Dict, Optional, Any
from loguru import logger
from rank_bm25 import BM25Okapi
import numpy as np


class BM25Retriever:
    """
    BM25 keyword-based retrieval
    Excellent for exact matches and keyword queries
    """
    
    def __init__(
        self,
        documents: List[Dict[str, Any]],
        k1: float = 1.5,
        b: float = 0.75,
        top_k: int = 10
    ):
        """
        Initialize BM25 retriever
        
        Args:
            documents: List of documents with 'id', 'content', and 'metadata'
            k1: BM25 term saturation parameter (typical: 1.2-2.0)
            b: BM25 length normalization parameter (typical: 0.75)
            top_k: Number of results to retrieve
        """
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.top_k = top_k
        
        # Tokenize documents
        self.tokenized_docs = [
            self._tokenize(doc["content"]) for doc in documents
        ]
        
        # Initialize BM25
        self.bm25 = BM25Okapi(
            self.tokenized_docs,
            k1=k1,
            b=b
        )
        
        logger.info(
            f"BM25Retriever initialized with {len(documents)} documents, "
            f"k1={k1}, b={b}"
        )
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using BM25
        
        Args:
            query: Search query
            top_k: Number of results (overrides default)
            
        Returns:
            List of retrieved documents with scores
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
        
        k = top_k or self.top_k
        
        # Tokenize query
        tokenized_query = self._tokenize(query)
        
        # Get BM25 scores
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        top_indices = np.argsort(scores)[::-1][:k]
        
        # Format results
        retrieved_docs = []
        for rank, idx in enumerate(top_indices):
            if scores[idx] <= 0:
                continue
            
            doc = {
                "id": self.documents[idx]["id"],
                "content": self.documents[idx]["content"],
                "metadata": self.documents[idx]["metadata"],
                "score": float(scores[idx]),
                "rank": rank + 1,
                "retrieval_method": "bm25"
            }
            retrieved_docs.append(doc)
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents via BM25")
        return retrieved_docs
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text for BM25
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Simple tokenization (can be improved with spaCy, NLTK, etc.)
        text = text.lower()
        
        # Remove punctuation and split
        import re
        tokens = re.findall(r'\b\w+\b', text)
        
        return tokens
    
    def update_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Update the document corpus
        
        Args:
            documents: New list of documents
        """
        self.documents = documents
        self.tokenized_docs = [
            self._tokenize(doc["content"]) for doc in documents
        ]
        self.bm25 = BM25Okapi(
            self.tokenized_docs,
            k1=self.k1,
            b=self.b
        )
        logger.info(f"Updated BM25 with {len(documents)} documents")


if __name__ == "__main__":
    # Test BM25 retriever
    docs = [
        {
            "id": "doc1",
            "content": "Machine learning is a subset of artificial intelligence",
            "metadata": {}
        },
        {
            "id": "doc2",
            "content": "Deep learning uses neural networks to learn patterns",
            "metadata": {}
        },
        {
            "id": "doc3",
            "content": "Natural language processing helps computers understand text",
            "metadata": {}
        }
    ]
    
    retriever = BM25Retriever(documents=docs, top_k=2)
    results = retriever.retrieve("machine learning neural networks")
    
    print(f"Retrieved {len(results)} documents")
    for doc in results:
        print(f"  - {doc['id']}: {doc['score']:.4f}")
