"""
ChromaDB Store
Vector database implementation using ChromaDB
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import chromadb
from chromadb.config import Settings
from loguru import logger

from ..chunking.base_chunker import Chunk


class ChromaStore:
    """
    Production-grade ChromaDB vector store
    Handles document storage, retrieval, and management
    """
    
    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: str = "./data/chroma_db",
        distance_metric: str = "cosine"
    ):
        """
        Initialize ChromaDB store
        
        Args:
            collection_name: Name of the collection
            persist_directory: Directory for persistent storage
            distance_metric: Distance metric (cosine, l2, ip)
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.distance_metric = distance_metric
        
        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Map distance metrics to ChromaDB space names
        metric_map = {
            "cosine": "cosine",
            "l2": "l2",
            "ip": "ip"  # Inner product
        }
        
        if distance_metric not in metric_map:
            raise ValueError(
                f"Invalid distance metric: {distance_metric}. "
                f"Choose from: {list(metric_map.keys())}"
            )
        
        # Get or create collection using the modern API
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": metric_map[distance_metric]}
        )
        logger.info(f"Collection ready: {collection_name}")
    
    def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]]
    ) -> None:
        """
        Add chunks with embeddings to the store
        
        Args:
            chunks: List of Chunk objects
            embeddings: List of embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        if not chunks:
            logger.warning("No chunks to add")
            return
        
        # Prepare data for ChromaDB
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.success(f"Added {len(chunks)} chunks to collection")
        except Exception as e:
            logger.error(f"Error adding chunks to store: {e}")
            raise
    
    def query(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Query the store for similar vectors
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            Query results with documents, distances, and metadata
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = {
                "ids": results["ids"][0],
                "documents": results["documents"][0],
                "distances": results["distances"][0],
                "metadatas": results["metadatas"][0]
            }
            
            logger.debug(f"Retrieved {len(formatted_results['ids'])} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying store: {e}")
            raise
    
    def get_by_ids(self, ids: List[str]) -> Dict[str, Any]:
        """
        Retrieve documents by IDs
        
        Args:
            ids: List of document IDs
            
        Returns:
            Retrieved documents and metadata
        """
        try:
            results = self.collection.get(
                ids=ids,
                include=["documents", "embeddings", "metadatas"]
            )
            return results
        except Exception as e:
            logger.error(f"Error retrieving by IDs: {e}")
            raise
    
    def delete_by_ids(self, ids: List[str]) -> None:
        """
        Delete documents by IDs
        
        Args:
            ids: List of document IDs to delete
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from collection")
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise
    
    def count(self) -> int:
        """
        Get the total number of documents in the collection
        
        Returns:
            Document count
        """
        return self.collection.count()
    
    def reset(self) -> None:
        """
        Reset the collection (delete all documents)
        
        WARNING: This will delete all documents in the collection!
        """
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            logger.warning(f"Reset collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            raise
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the database
        
        Returns:
            List of collection names
        """
        collections = self.client.list_collections()
        return [col.name for col in collections]


if __name__ == "__main__":
    # Test the ChromaDB store
    store = ChromaStore(
        collection_name="test_collection",
        persist_directory="./test_data/chroma"
    )
    
    print(f"Collection count: {store.count()}")
    print(f"Available collections: {store.list_collections()}")
