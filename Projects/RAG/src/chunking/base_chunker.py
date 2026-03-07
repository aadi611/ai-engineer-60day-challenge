"""
Base Chunker
Abstract base class for all chunking strategies
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class Chunk:
    """
    Represents a text chunk with metadata
    """
    content: str
    chunk_id: str
    metadata: Dict
    start_index: int = 0
    end_index: int = 0
    
    def __len__(self) -> int:
        return len(self.content)
    
    def __repr__(self) -> str:
        return f"Chunk(id={self.chunk_id}, length={len(self.content)})"


class BaseChunker(ABC):
    """
    Abstract base class for document chunking strategies
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target size for each chunk
            chunk_overlap: Number of characters to overlap between chunks
            min_chunk_size: Minimum size for a valid chunk
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        
        self._validate_params()
    
    def _validate_params(self):
        """Validate chunking parameters"""
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        if self.min_chunk_size <= 0:
            raise ValueError("min_chunk_size must be positive")
    
    @abstractmethod
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """
        Chunk text into segments
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to all chunks
            
        Returns:
            List of Chunk objects
        """
        pass
    
    def _create_chunk(
        self,
        content: str,
        index: int,
        metadata: Dict,
        start_index: int = 0,
        end_index: int = 0
    ) -> Chunk:
        """
        Create a Chunk object with proper metadata
        """
        import uuid
        chunk_metadata = {
            **metadata,
            "chunk_index": index,
            "chunk_size": len(content),
            "start_index": start_index,
            "end_index": end_index
        }
        
        # Use doc_id from metadata if available, else generate a unique UUID
        doc_id = metadata.get('doc_id') or str(uuid.uuid4())
        chunk_id = f"{doc_id}_{index}"
        
        return Chunk(
            content=content,
            chunk_id=chunk_id,
            metadata=chunk_metadata,
            start_index=start_index,
            end_index=end_index
        )
    
    def _filter_small_chunks(self, chunks: List["Chunk"]) -> List["Chunk"]:
        """
        Filter out chunks that are too small
        
        Args:
            chunks: List of chunks
            
        Returns:
            Filtered list of chunks
        """
        filtered = [c for c in chunks if len(c.content) >= self.min_chunk_size]
        
        if len(filtered) < len(chunks):
            logger.debug(
                f"Filtered out {len(chunks) - len(filtered)} chunks "
                f"smaller than {self.min_chunk_size} characters"
            )
        
        return filtered
