import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticCache:
    def __init__(self, similarity_threshold=0.85, ttl=300):
        """
        similarity_threshold: how close prompts should be (0–1)
        ttl: time to live (seconds)
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = []
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl

    def _get_embedding(self, text):
        return self.model.encode([text])[0]

    def get(self, prompt):
        prompt_embedding = self._get_embedding(prompt)

        for entry in self.cache:
            # Check expiry
            if time.time() - entry["timestamp"] > self.ttl:
                continue

            similarity = cosine_similarity(
                [prompt_embedding],
                [entry["embedding"]]
            )[0][0]

            if similarity >= self.similarity_threshold:
                print(f"✅ Semantic Cache HIT (score={similarity:.2f})")
                return entry["response"]

        print("❌ Cache MISS")
        return None

    def set(self, prompt, response):
        embedding = self._get_embedding(prompt)

        self.cache.append({
            "prompt": prompt,
            "embedding": embedding,
            "response": response,
            "timestamp": time.time()
        })


# ------------------ Usage ------------------

def fake_llm_call(prompt):
    return f"Generated response for: {prompt}"


cache = SemanticCache(similarity_threshold=0.85, ttl=300)


def get_response(prompt):
    cached = cache.get(prompt)
    if cached:
        return cached

    response = fake_llm_call(prompt)
    cache.set(prompt, response)
    return response


# ------------------ Test ------------------

print(get_response("Explain AI agents"))
print(get_response("What are AI agents?"))  # Should HIT
