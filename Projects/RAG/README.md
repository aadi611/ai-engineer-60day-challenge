# 🚀 Production RAG System

A production-grade Retrieval-Augmented Generation (RAG) system built with Python, incorporating all advanced concepts from Week 1 of the AI Engineer Challenge.

## ⚡ Key Features

### 📚 Document Processing
- **Multi-format support**: PDF, TXT, Markdown, DOCX
- **Intelligent preprocessing**: Text cleaning and normalization
- **Robust error handling**: Gracefully handles malformed documents

### ✂️ Advanced Chunking Strategies
- **Fixed-size chunking**: Simple and fast with configurable overlap
- **Semantic chunking**: Embedding-based topic boundary detection
- **Recursive chunking**: Hierarchical splitting preserving document structure

### 🔍 Hybrid Search
- **Vector search**: Dense embeddings for semantic similarity
- **BM25 search**: Sparse keyword-based retrieval
- **Reciprocal Rank Fusion (RRF)**: Intelligent result fusion
- **Weighted combination**: Configurable alpha blending

### 🎯 Reranking
- **Cross-encoder reranking**: ms-marco-MiniLM-L-6-v2
- **Improved relevance**: More accurate than bi-encoder similarity
- **Configurable top-k**: Return most relevant documents

### 💾 Vector Storage
- **ChromaDB integration**: Persistent vector database
- **Collection management**: Organize documents by domain
- **Metadata filtering**: Filter by document attributes
- **Distance metrics**: Cosine, L2, Inner Product

### 🤖 LLM Generation
- **OpenAI GPT-4**: State-of-the-art response generation
- **Context grounding**: Responses backed by retrieved documents
- **Citation support**: Source attribution for transparency
- **Streaming support**: Real-time response generation

### 📊 Comprehensive Evaluation
- **Retrieval metrics**: Precision@K, Recall@K, F1, MRR, NDCG
- **Answer quality**: Context overlap, faithfulness, relevance
- **Batch evaluation**: Automated testing at scale

## 📁 Project Structure

```
RAG/
├── config/
│   └── config.yaml              # System configuration
├── src/
│   ├── __init__.py
│   ├── document_loader.py       # Document ingestion
│   ├── chunking/               # Chunking strategies
│   │   ├── __init__.py
│   │   ├── base_chunker.py
│   │   ├── fixed_chunker.py
│   │   ├── semantic_chunker.py
│   │   └── recursive_chunker.py
│   ├── embeddings/             # Embedding generation
│   │   ├── __init__.py
│   │   └── embedding_generator.py
│   ├── storage/                # Vector database
│   │   ├── __init__.py
│   │   └── chroma_store.py
│   ├── retrieval/              # Search strategies
│   │   ├── __init__.py
│   │   ├── vector_retriever.py
│   │   ├── bm25_retriever.py
│   │   ├── hybrid_retriever.py
│   │   └── reranker.py
│   ├── generation/             # LLM response generation
│   │   ├── __init__.py
│   │   └── llm_generator.py
│   ├── evaluation/             # Evaluation metrics
│   │   ├── __init__.py
│   │   └── metrics.py
│   └── pipeline.py             # Main RAG orchestration
├── chatbot.py                  # Interactive chatbot interface
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🛠️ Setup

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd Projects/RAG
```

2. **Create a virtual environment**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Quick Start

### Interactive Chatbot

The easiest way to use the RAG system:

```bash
python chatbot.py
```

#### Chatbot Commands:
- `/ingest <path>` - Ingest documents from a file or directory
- `/stats` - Show system statistics
- `/reset` - Reset the system (clear all documents)
- `/help` - Show help message
- `/quit` or `/exit` - Exit the chatbot

#### Example Session:
```
You: /ingest ./documents
✓ Successfully ingested 5 documents!

You: What is machine learning?
Answer: Machine learning is a subset of artificial intelligence...
[Sources: document1.pdf, document2.txt]

You: /stats
System Statistics:
- Total Chunks: 150
- Retrieval Strategy: hybrid
...
```

### Programmatic Usage

```python
from src.pipeline import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline(config_path="config/config.yaml")

# Ingest documents
pipeline.ingest_documents(directory_path="./documents")

# Query the system
result = pipeline.query("What is retrieval-augmented generation?")

print(result["response"])
print(f"Sources: {len(result['sources'])}")
```

## ⚙️ Configuration

Edit `config/config.yaml` to customize the system:

```yaml
# Chunking
chunking:
  strategy: "recursive"  # Options: fixed, semantic, recursive
  chunk_size: 500
  chunk_overlap: 50

# Retrieval
retrieval:
  strategy: "hybrid"  # Options: vector, bm25, hybrid
  top_k: 10
  hybrid:
    fusion_method: "rrf"  # Options: rrf, weighted
    alpha: 0.5

# Reranking
reranking:
  enabled: true
  top_k: 5

# LLM
llm:
  model: "gpt-4-turbo-preview"
  temperature: 0.7
  max_tokens: 1000
```

## 📊 Evaluation

Evaluate your RAG system:

```python
from src.evaluation import RAGEvaluator

evaluator = RAGEvaluator()

# Evaluate retrieval
metrics = evaluator.evaluate_retrieval(
    retrieved_docs=["doc1", "doc2", "doc3"],
    relevant_docs=["doc1", "doc3", "doc5"]
)

print(f"Precision@3: {metrics['precision@3']:.4f}")
print(f"Recall@3: {metrics['recall@3']:.4f}")
print(f"MRR: {metrics['mrr']:.4f}")
print(f"NDCG@10: {metrics['ndcg@10']:.4f}")
```

## 🏗️ Architecture

### RAG Pipeline Flow

```
Document Ingestion
    ↓
Text Preprocessing
    ↓
Chunking (Fixed/Semantic/Recursive)
    ↓
Embedding Generation
    ↓
Vector Storage (ChromaDB)
    ↓
User Query
    ↓
Hybrid Search (Vector + BM25)
    ↓
RRF Fusion
    ↓
Cross-Encoder Reranking
    ↓
Context Assembly
    ↓
LLM Generation (GPT-4)
    ↓
Response with Citations
```

## 🎯 Week 1 Concepts Implemented

### Day 1: Search Fundamentals
- ✅ Vector embeddings (OpenAI text-embedding-3-small)
- ✅ Similarity metrics (Cosine, L2, Inner Product)
- ✅ Semantic search implementation

### Day 2: Basic RAG Pipeline
- ✅ Document loading and preprocessing
- ✅ Embedding generation
- ✅ Vector storage setup
- ✅ Query processing
- ✅ Response generation with LLMs

### Day 3: ChromaDB Integration
- ✅ Collection management
- ✅ Metadata filtering
- ✅ Persistent storage configuration
- ✅ Distance metrics
- ✅ Batch operations

### Day 4: Advanced Chunking
- ✅ Fixed-size chunking
- ✅ Semantic chunking with embeddings
- ✅ Recursive character splitting
- ✅ Metadata-aware chunking
- ✅ Context preservation

### Day 5: Hybrid Search
- ✅ BM25 implementation
- ✅ Vector search
- ✅ Reciprocal Rank Fusion (RRF)
- ✅ Weighted score combination
- ✅ Configurable fusion strategies

### Day 6: RAG Evaluation
- ✅ Precision@K, Recall@K, F1
- ✅ Mean Reciprocal Rank (MRR)
- ✅ Normalized Discounted Cumulative Gain (NDCG)
- ✅ Answer quality metrics
- ✅ Automated evaluation pipelines

### Day 7: Integration & Best Practices
- ✅ End-to-end RAG pipeline
- ✅ Production-grade error handling
- ✅ Comprehensive logging
- ✅ Configuration management
- ✅ Interactive chatbot interface

## 🔧 Advanced Features

### Custom Chunking Strategy

```python
from src.chunking import RecursiveChunker

chunker = RecursiveChunker(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " "]
)

chunks = chunker.chunk(text, metadata={"source": "doc1"})
```

### Custom Retrieval

```python
# Vector-only retrieval
result = pipeline.query(
    "What is AI?",
    retrieval_strategy="vector",
    top_k=5
)

# Hybrid with custom fusion
result = pipeline.query(
    "Machine learning basics",
    retrieval_strategy="hybrid"
)
```

### Streaming Responses

```python
for chunk in pipeline.llm_generator.generate_streaming(
    query="Explain RAG",
    retrieved_docs=docs
):
    print(chunk, end="", flush=True)
```

## 📈 Performance Optimization

### Tips for Production
1. **Batch document ingestion** for faster processing
2. **Use fixed chunking** for speed, semantic for quality
3. **Enable reranking** for critical applications
4. **Tune hybrid alpha** based on your use case (0.5 is a good start)
5. **Monitor context length** to stay within LLM limits
6. **Cache embeddings** for frequently reused documents

### Benchmarks
- **Ingestion**: ~50 docs/minute (varies by size)
- **Retrieval**: ~100ms (hybrid with reranking)
- **Generation**: ~2-5s (depends on LLM response length)

## 🐛 Troubleshooting

### Common Issues

**ChromaDB persistence errors:**
```bash
# Delete and recreate the database
rm -rf data/chroma_db
```

**Out of memory during ingestion:**
```yaml
# Reduce chunk size in config.yaml
chunking:
  chunk_size: 300  # Smaller chunks
```

**Slow retrieval:**
```yaml
# Disable reranking or reduce top_k
reranking:
  enabled: false
retrieval:
  top_k: 5
```

## 🤝 Contributing

This is a learning project, but improvements are welcome!

## 📝 License

MIT License - Feel free to use for learning and production!

## 🙏 Acknowledgments

Built as part of the 60-Day AI Engineer Challenge, incorporating:
- OpenAI GPT-4 and Embeddings
- ChromaDB for vector storage
- HuggingFace Transformers for reranking
- LangChain concepts and patterns

## 📚 Additional Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [RAG Best Practices](https://arxiv.org/abs/2312.10997)
- [BM25 Algorithm](https://en.wikipedia.org/wiki/Okapi_BM25)

---

**Built with ❤️ for production AI systems**
