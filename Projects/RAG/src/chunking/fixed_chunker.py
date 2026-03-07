"""
Fixed Size Chunker
Simple chunking with fixed size and overlap
"""

from typing import List, Dict, Optional
from loguru import logger

from .base_chunker import BaseChunker, Chunk


class FixedSizeChunker(BaseChunker):
    """
    Fixed-size chunking with overlap
    Simple and fast, good for general use
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        super().__init__(chunk_size, chunk_overlap, min_chunk_size)
        logger.info(
            f"FixedSizeChunker initialized: "
            f"size={chunk_size}, overlap={chunk_overlap}"
        )
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """
        Chunk text into fixed-size segments with overlap
        
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
        chunks = []
        
        start = 0
        index = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position
            end = min(start + self.chunk_size, text_length)
            
            # Extract chunk content
            chunk_content = text[start:end].strip()
            
            # Create chunk if content is valid
            if len(chunk_content) >= self.min_chunk_size:
                chunk = self._create_chunk(
                    content=chunk_content,
                    index=index,
                    metadata=metadata,
                    start_index=start,
                    end_index=end
                )
                chunks.append(chunk)
                index += 1
            
            # Move to next position with overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start <= end - self.chunk_size:
                start = end
        
        logger.info(f"Created {len(chunks)} fixed-size chunks from text")
        return chunks


if __name__ == "__main__":
    # Test the chunker
    chunker = FixedSizeChunker(chunk_size=100, chunk_overlap=20)
    
    test_text = "This is a sample text. " * 50
    chunks = chunker.chunk(test_text, metadata={"doc_id": "test_doc"})
    
    print(f"Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i}: {chunk.content[:50]}...")
