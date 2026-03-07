"""
Recursive Character Chunker
Hierarchical chunking with fallback separators
"""

from typing import List, Dict, Optional
from loguru import logger

from .base_chunker import BaseChunker, Chunk


class RecursiveChunker(BaseChunker):
    """
    Recursive character text splitting
    Tries to split on larger separators first, falls back to smaller ones
    Best for maintaining document structure
    """
    
    DEFAULT_SEPARATORS = [
        "\n\n",  # Paragraph breaks
        "\n",    # Line breaks
        ". ",    # Sentence ends
        "! ",    # Exclamation sentence ends
        "? ",    # Question sentence ends
        "; ",    # Semicolons
        ", ",    # Commas
        " ",     # Spaces
        ""       # Characters
    ]
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize recursive chunker
        
        Args:
            chunk_size: Target chunk size
            chunk_overlap: Overlap between chunks
            min_chunk_size: Minimum chunk size
            separators: List of separators to try (in order of preference)
        """
        super().__init__(chunk_size, chunk_overlap, min_chunk_size)
        self.separators = separators or self.DEFAULT_SEPARATORS
        
        logger.info(
            f"RecursiveChunker initialized with "
            f"{len(self.separators)} separator levels"
        )
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """
        Recursively chunk text using hierarchical separators
        
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
        
        # Recursively split the text
        splits = self._recursive_split(text, self.separators)
        
        # Merge splits into chunks with overlap
        chunks = self._merge_splits_into_chunks(splits, metadata)
        
        # Filter small chunks
        chunks = self._filter_small_chunks(chunks)
        
        logger.info(f"Created {len(chunks)} recursive chunks from text")
        return chunks
    
    def _recursive_split(
        self,
        text: str,
        separators: List[str]
    ) -> List[str]:
        """
        Recursively split text using separators
        
        Args:
            text: Text to split
            separators: List of separators to try
            
        Returns:
            List of text segments
        """
        if not separators:
            # No more separators, return text as-is
            return [text] if text else []
        
        # Try current separator
        separator = separators[0]
        remaining_separators = separators[1:]
        
        if separator == "":
            # Character-level split
            return list(text)
        
        # Split on current separator
        splits = text.split(separator)
        
        # Keep separator with splits (except last one)
        result = []
        for i, split in enumerate(splits):
            if i < len(splits) - 1:
                split = split + separator
            
            if split:
                # If split is still too large, recursively split it
                if len(split) > self.chunk_size:
                    sub_splits = self._recursive_split(split, remaining_separators)
                    result.extend(sub_splits)
                else:
                    result.append(split)
        
        return result
    
    def _merge_splits_into_chunks(
        self,
        splits: List[str],
        metadata: Dict
    ) -> List[Chunk]:
        """
        Merge splits into chunks of appropriate size with overlap
        
        Args:
            splits: List of text splits
            metadata: Chunk metadata
            
        Returns:
            List of Chunk objects
        """
        chunks = []
        current_chunk = []
        current_size = 0
        index = 0
        
        for split in splits:
            split_size = len(split)
            
            # Check if adding this split would exceed chunk size
            if current_size + split_size > self.chunk_size and current_chunk:
                # Create chunk from accumulated splits
                content = ''.join(current_chunk).strip()
                
                if content:
                    chunk = self._create_chunk(
                        content=content,
                        index=index,
                        metadata=metadata
                    )
                    chunks.append(chunk)
                    index += 1
                
                # Calculate overlap
                overlap_size = 0
                overlap_chunks = []
                
                # Take splits from the end for overlap
                for i in range(len(current_chunk) - 1, -1, -1):
                    overlap_size += len(current_chunk[i])
                    overlap_chunks.insert(0, current_chunk[i])
                    
                    if overlap_size >= self.chunk_overlap:
                        break
                
                # Start new chunk with overlap
                current_chunk = overlap_chunks
                current_size = overlap_size
            
            current_chunk.append(split)
            current_size += split_size
        
        # Add final chunk
        if current_chunk:
            content = ''.join(current_chunk).strip()
            if content:
                chunk = self._create_chunk(
                    content=content,
                    index=index,
                    metadata=metadata
                )
                chunks.append(chunk)
        
        return chunks


if __name__ == "__main__":
    # Test the chunker
    chunker = RecursiveChunker(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    test_text = """
    This is the first paragraph. It contains multiple sentences. Each sentence adds information.
    
    This is the second paragraph. It discusses a different topic. The recursive chunker will try to keep paragraphs together.
    
    This is the third paragraph. It demonstrates how the chunker works with hierarchical separators.
    """
    
    chunks = chunker.chunk(test_text, metadata={"doc_id": "test_doc"})
    
    print(f"Created {len(chunks)} recursive chunks")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} (length: {len(chunk.content)}) ---")
        print(chunk.content)
