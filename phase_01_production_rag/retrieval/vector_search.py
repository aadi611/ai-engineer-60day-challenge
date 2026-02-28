# Vector Search Implementation
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorSearch:
    def __init__(self, documents):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = documents

        self.embeddings = self.model.encode(documents)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def search(self, query, top_k=3):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array([query_vector]), top_k)

        results = [(self.documents[i], float(distances[0][rank]))
                    for rank, i in enumerate(indices[0])]
        
        return results