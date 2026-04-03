# Metadata Enrichment for Chunks
import uuid
import time


class MetadataChunker:
    def __init__(self, chunk_size=200, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_with_metadata(self, text, source="unknown"):
        words = text.split()
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            metadata = {
                "id": str(uuid.uuid4()),
                "chunk_index": chunk_id,
                "source": source,
                "start_word": start,
                "end_word": end,
                "length": len(chunk_words),
                "created_at": time.time()
            }

            chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })

            chunk_id += 1
            start += self.chunk_size - self.overlap

        return chunks


# ------------------ Usage ------------------

text = """
Artificial Intelligence is transforming industries by enabling machines 
to learn from data and make decisions. Machine learning, deep learning, 
and natural language processing are key areas of AI.
"""

chunker = MetadataChunker(chunk_size=10, overlap=3)

chunks = chunker.chunk_with_metadata(text, source="ai_article.txt")

for chunk in chunks:
    print("TEXT:", chunk["text"])
    print("METADATA:", chunk["metadata"])
    print("-" * 50)