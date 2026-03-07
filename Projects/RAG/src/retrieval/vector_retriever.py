"""
Vector Retriever
Dense vector-based semantic search
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from ..storage.chroma_store import ChromaStore
from ..embeddings.embedding_generator import EmbeddingGenerator


class VectorRetriever:
    """
    Vector-based semantic retrieval using embeddings
    """
    
    def __init__(
        self,
        store: ChromaStore,
        embedding_generator: EmbeddingGenerator,
        top_k: int = 10,
        similarity_threshold: float = 0.0
    ):
        """
        Initialize vector retriever
        
        Args:
            store: ChromaDB store
            embedding_generator: Embedding generator
            top_k: Number of results to retrieve
            similarity_threshold: Minimum similarity score
        """
        self.store = store
        self.embedding_generator = embedding_generator
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        
        logger.info(f"VectorRetriever initialized with top_k={top_k}")
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using vector similarity
        
        Args:
            query: Search query
            top_k: Number of results (overrides default)
            filter_metadata: Optional metadata filter
            
        Returns:
            List of retrieved documents with scores
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []
        
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedding_generator.embed(query)
        
        # Search in vector store
        results = self.store.query(
            query_embedding=query_embedding,
            top_k=k,
            filter_metadata=filter_metadata
        )
        
        # Format results
        retrieved_docs = []
        for i in range(len(results["ids"])):
            # Convert distance to similarity score (for cosine distance)
            # ChromaDB returns distance, lower is better
            # For cosine: similarity = 1 - distance
            distance = results["distances"][i]
            similarity = 1.0 - distance
            
            # Filter by similarity threshold
            if similarity < self.similarity_threshold:
                continue
            
            doc = {
                "id": results["ids"][i],
                "content": results["documents"][i],
                "metadata": results["metadatas"][i],
                "score": similarity,
                "rank": i + 1,
                "retrieval_method": "vector"
            }
            retrieved_docs.append(doc)
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents via vector search")
        return retrieved_docs


if __name__ == "__main__":
    print("VectorRetriever module ready")
