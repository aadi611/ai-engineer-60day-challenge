"""
Embedding Generator
Generates vector embeddings for text using various models
"""

from typing import List, Union, Optional
import numpy as np
from loguru import logger
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

# Explicitly point to the .env file in the project root (Projects/RAG/.env)
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env", override=True)


class EmbeddingGenerator:
    """
    Production-grade embedding generator supporting multiple models
    """
    
    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        batch_size: int = 100,
        dimensions: Optional[int] = None
    ):
        """
        Initialize embedding generator
        
        Args:
            model: Name of the embedding model
            api_key: OpenAI API key (if using OpenAI models)
            batch_size: Batch size for processing multiple texts
            dimensions: Embedding dimensions (for models that support it)
        """
        self.model = model
        self.batch_size = batch_size
        self.dimensions = dimensions
        
        # Initialize client based on model type
        if "text-embedding" in model:
            # OpenAI embeddings
            self.client = OpenAI(api_key=api_key)
            self.provider = "openai"
        else:
            # Could add support for other providers (Cohere, HuggingFace, etc.)
            raise ValueError(f"Unsupported embedding model: {model}")
        
        logger.info(f"EmbeddingGenerator initialized with model: {model}")
    
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text
        
        Args:
            text: Single text string or list of texts
            
        Returns:
            Embedding vector(s)
        """
        # Handle single text vs list
        if isinstance(text, str):
            texts = [text]
            return_single = True
        else:
            texts = text
            return_single = False
        
        if not texts:
            logger.warning("Empty text list provided to embed()")
            return [] if not return_single else [0.0] * (self.dimensions or 1536)
        
        # Generate embeddings in batches
        all_embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_embeddings = self._embed_batch(batch)
            all_embeddings.extend(batch_embeddings)
        
        logger.debug(f"Generated embeddings for {len(texts)} texts")
        
        return all_embeddings[0] if return_single else all_embeddings
    
    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts: List of texts
            
        Returns:
            List of embedding vectors
        """
        if self.provider == "openai":
            return self._embed_openai(texts)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI API
        
        Args:
            texts: List of texts
            
        Returns:
            List of embedding vectors
        """
        try:
            # Prepare parameters
            params = {
                "model": self.model,
                "input": texts
            }
            
            # Add dimensions if specified
            if self.dimensions is not None:
                params["dimensions"] = self.dimensions
            
            # Call API
            response = self.client.embeddings.create(**params)
            
            # Extract embeddings
            embeddings = [item.embedding for item in response.data]
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model
        
        Returns:
            Embedding dimension
        """
        if self.dimensions:
            return self.dimensions
        
        # Default dimensions for common models
        dimension_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        
        return dimension_map.get(self.model, 1536)
    
    def cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm_product = np.linalg.norm(vec1_np) * np.linalg.norm(vec2_np)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)


if __name__ == "__main__":
    # Test the embedding generator
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    generator = EmbeddingGenerator(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Test single text
    text = "This is a test sentence."
    embedding = generator.embed(text)
    print(f"Generated embedding of dimension: {len(embedding)}")
    
    # Test similarity
    text2 = "This is another test sentence."
    embedding2 = generator.embed(text2)
    similarity = generator.cosine_similarity(embedding, embedding2)
    print(f"Similarity between texts: {similarity:.4f}")
