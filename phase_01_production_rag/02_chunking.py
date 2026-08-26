"""Step 2: load documents and split them into chunks.

Still no embeddings/vector store yet -- just the loading + chunking stage
of the RAG pipeline, so you can see how chunk size/overlap affects the
resulting chunks before adding retrieval on top.
"""

from pathlib import Path
import time

from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path(__file__).parent / "data"


def load_documents() -> list[dict]:
    """Read every .txt file in data/ into {"source": filename, "text": contents}."""
    docs = []
    for path in sorted(DATA_DIR.glob("*.txt")):
        docs.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
    return docs


def chunk_documents(docs: list[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """Split each document's text into overlapping chunks, keeping the source name attached."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = []
    for doc in docs:
        for i, piece in enumerate(splitter.split_text(doc["text"])):
            chunks.append({"source": doc["source"], "chunk_id": i, "text": piece})
    return chunks


if __name__ == "__main__":
    documents = load_documents()
    print(f"Loaded {len(documents)} documents: {[d['source'] for d in documents]}\n")

    chunks = chunk_documents(documents)
    print(f"Produced {len(chunks)} chunks\n")

    for c in chunks:
        print(f"--- {c['source']} #{c['chunk_id']} ({len(c['text'])} chars) ---")
        print(c["text"])
        print()
