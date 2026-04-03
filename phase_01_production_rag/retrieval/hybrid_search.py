# Hybrid Search Implementation
from retrieval.vector_search import VectorSearch
from retrieval.bm25_search import BM25Search

class HybridSearch:
    def __init__(self, documents):
        self.vector = VectorSearch(documents)
        self.keyword = BM25Search(documents)

    def search(self, query, top_k=3):
        vec_results = self.vector.search(query, top_k)
        key_results = self.keyword.search(query, top_k)

        scores = {}

        for doc, score in vec_results:
            scores[doc] = scores.get(doc, 0) + (1 / (1 + score))

        for doc, score in key_results:
            scores[doc] = scores.get(doc, 0) + score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]