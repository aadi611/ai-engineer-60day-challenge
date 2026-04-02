# Fixed Chunking Implementation
class FixedChunker:
    def __init__(self, chunk_size=200, overlap=50):
        """
        chunk_size: number of words per chunk
        overlap: number of overlapping words between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text):
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append(chunk_text)

            # move with overlap
            start += self.chunk_size - self.overlap

        return chunks


# ------------------ Usage ------------------

text = """
Artificial Intelligence is transforming industries by enabling machines 
to learn from data and make decisions. Machine learning, deep learning, 
and natural language processing are key areas of AI.
"""

chunker = FixedChunker(chunk_size=10, overlap=3)

chunks = chunker.chunk(text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}\n")