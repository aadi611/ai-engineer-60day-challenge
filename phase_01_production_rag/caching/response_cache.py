# Response Cache Implementation
import hashlib
import time

class ResponseCache:
    def __init__(self, ttl=300):
        """
        ttl: time to live in seconds (default 5 mins)
        """
        self.cache = {}
        self.ttl = ttl

    def _generate_key(self, prompt):
        """Create a unique hash key for each prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()

    def get(self, prompt):
        key = self._generate_key(prompt)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check expiry
            if time.time() - entry["timestamp"] < self.ttl:
                print("✅ Cache HIT")
                return entry["response"]
            else:
                print("⏳ Cache EXPIRED")
                del self.cache[key]

        print("❌ Cache MISS")
        return None

    def set(self, prompt, response):
        key = self._generate_key(prompt)
        
        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }
        
        
######Usage Example with LLM
def fake_llm_call(prompt):
    # Replace this with OpenAI / any LLM API
    return f"Generated response for: {prompt}"

cache = ResponseCache(ttl=300)

def get_response(prompt):
    # Step 1: Check cache
    cached = cache.get(prompt)
    if cached:
        return cached

    # Step 2: Call LLM
    response = fake_llm_call(prompt)

    # Step 3: Store in cache
    cache.set(prompt, response)

    return response


# Test
print(get_response("Explain AI agents"))
print(get_response("Explain AI agents"))  # Should hit cache


