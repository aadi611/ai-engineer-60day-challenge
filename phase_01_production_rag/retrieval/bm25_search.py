# BM25 Search Implementation
from rank_bm25 import BM25Okapi

class BM25Search:
    def __init__(self, documents):
        self.documents = documents
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, top_k=3):
        scores = self.bm25.get_scores(query.lower().split())
        ranked = sorted(zip(self.documents, scores),
                        key=lambda x: x[1],
                        reverse=True)
        return ranked[:top_k]