"""
Semantic Chunker
Chunks text based on semantic boundaries using embeddings
"""

from typing import List, Dict, Optional
import numpy as np
from loguru import logger

from .base_chunker import BaseChunker, Chunk


class SemanticChunker(BaseChunker):
    """
    Semantic chunking using embeddings to detect topic shifts
    More sophisticated but computationally expensive
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
        embedding_model=None,
        similarity_threshold: float = 0.7
    ):
        """
        Initialize semantic chunker
        
        Args:
            chunk_size: Target chunk size
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size
            embedding_model: Model for generating embeddings
            similarity_threshold: Threshold for detecting topic shifts
        """
        super().__init__(chunk_size, chunk_overlap, min_chunk_size)
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        
        logger.info(
            f"SemanticChunker initialized with "
            f"similarity_threshold={similarity_threshold}"
        )
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """
        Chunk text based on semantic boundaries
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of Chunk objects
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to chunker")
            return []
        
        metadata = metadata or {}
        
        # Split text into sentences first
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            logger.warning("No sentences found in text")
            return []
        
        # If no embedding model, fall back to sentence-based chunking
        if self.embedding_model is None:
            logger.warning("No embedding model provided, using sentence-based chunking")
            return self._sentence_based_chunking(sentences, metadata)
        
        # Generate embeddings for sentences
        try:
            embeddings = self._generate_embeddings(sentences)
            
            # Find semantic boundaries
            boundaries = self._find_semantic_boundaries(embeddings)
            
            # Create chunks based on boundaries
            chunks = self._create_chunks_from_boundaries(
                sentences, boundaries, metadata
            )
            
            logger.info(f"Created {len(chunks)} semantic chunks from text")
            return chunks
            
        except Exception as e:
            logger.error(f"Error in semantic chunking: {e}, falling back to sentence-based")
            return self._sentence_based_chunking(sentences, metadata)
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with spaCy or NLTK)
        import re
        
        # Split on sentence boundaries
        sentences = re.split(r'[.!?]+\s+', text)
        
        # Clean and filter
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _generate_embeddings(self, sentences: List[str]) -> np.ndarray:
        """
        Generate embeddings for sentences
        
        Args:
            sentences: List of sentences
            
        Returns:
            Array of embeddings
        """
        if hasattr(self.embedding_model, 'encode'):
            # sentence-transformers interface
            embeddings = self.embedding_model.encode(sentences)
            return np.array(embeddings)
        else:
            raise ValueError("Embedding model must have 'encode' method")
    
    def _find_semantic_boundaries(self, embeddings: np.ndarray) -> List[int]:
        """
        Find boundaries based on embedding similarity
        
        Args:
            embeddings: Sentence embeddings
            
        Returns:
            List of boundary indices
        """
        boundaries = [0]
        
        for i in range(1, len(embeddings)):
            # Calculate cosine similarity between consecutive sentences
            similarity = self._cosine_similarity(
                embeddings[i-1], embeddings[i]
            )
            
            # If similarity drops below threshold, it's a boundary
            if similarity < self.similarity_threshold:
                boundaries.append(i)
        
        boundaries.append(len(embeddings))
        
        return boundaries
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        
        if norm_product == 0:
            return 0.0
        
        return dot_product / norm_product
    
    def _create_chunks_from_boundaries(
        self,
        sentences: List[str],
        boundaries: List[int],
        metadata: Dict
    ) -> List[Chunk]:
        """
        Create chunks based on semantic boundaries
        
        Args:
            sentences: List of sentences
            boundaries: List of boundary indices
            metadata: Chunk metadata
            
        Returns:
            List of Chunk objects
        """
        chunks = []
        
        for i in range(len(boundaries) - 1):
            start_idx = boundaries[i]
            end_idx = boundaries[i + 1]
            
            # Combine sentences in this segment
            segment_sentences = sentences[start_idx:end_idx]
            content = ' '.join(segment_sentences)
            
            # Create chunk if it meets size requirements
            if len(content) >= self.min_chunk_size:
                chunk = self._create_chunk(
                    content=content,
                    index=i,
                    metadata=metadata,
                    start_index=start_idx,
                    end_index=end_idx
                )
                chunks.append(chunk)
        
        return chunks
    
    def _sentence_based_chunking(
        self,
        sentences: List[str],
        metadata: Dict
    ) -> List[Chunk]:
        """
        Simple sentence-based chunking fallback
        
        Args:
            sentences: List of sentences
            metadata: Chunk metadata
            
        Returns:
            List of Chunk objects
        """
        chunks = []
        current_chunk = []
        current_size = 0
        index = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > self.chunk_size and current_chunk:
                # Create chunk from accumulated sentences
                content = ' '.join(current_chunk)
                chunk = self._create_chunk(
                    content=content,
                    index=index,
                    metadata=metadata
                )
                chunks.append(chunk)
                index += 1
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_sentences
                current_size = sum(len(s) for s in overlap_sentences)
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add final chunk
        if current_chunk:
            content = ' '.join(current_chunk)
            if len(content) >= self.min_chunk_size:
                chunk = self._create_chunk(
                    content=content,
                    index=index,
                    metadata=metadata
                )
                chunks.append(chunk)
        
        return chunks


if __name__ == "__main__":
    # Test the chunker
    chunker = SemanticChunker(chunk_size=200, similarity_threshold=0.7)
    
    test_text = """
    Artificial intelligence is transforming the world. Machine learning is a subset of AI.
    Deep learning uses neural networks. These networks can learn complex patterns.
    
    Climate change is a global challenge. Rising temperatures affect ecosystems.
    We must reduce carbon emissions. Renewable energy is part of the solution.
    """
    
    chunks = chunker.chunk(test_text, metadata={"doc_id": "test_doc"})
    
    print(f"Created {len(chunks)} semantic chunks")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i}: {chunk.content}")
