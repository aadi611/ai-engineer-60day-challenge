# Day 2 - February 22, 2026

## Topics Covered
- Basic RAG Pipeline Architecture
- Document Loading and Preprocessing
- Text Chunking Implementation
- Embedding Generation
- Vector Storage Setup
- Query Processing
- Response Generation with LLMs
- End-to-End RAG Workflow

## What I Learned
- **RAG Pipeline Components**: Understanding the core components of a production RAG system
  - Document ingestion and preprocessing
  - Chunking strategies for optimal retrieval
  - Embedding generation for semantic search
  - Vector storage and indexing
  - Query processing and retrieval
  - Context injection and response generation
- **Document Loading**: Different methods to load and parse various document formats (PDF, TXT, Markdown)
- **Chunking Strategies**: 
  - Fixed-size chunking with overlap
  - Sentence-based chunking
  - Paragraph-based chunking
  - Trade-offs between chunk size and retrieval quality
- **Embedding Models**: Working with embedding models (e.g., OpenAI embeddings, sentence-transformers)
- **Context Window Management**: How to manage LLM context limits when injecting retrieved documents
- **Prompt Engineering for RAG**: Crafting effective prompts that incorporate retrieved context

## Code/Projects
- Implemented basic RAG pipeline in `phase_01_production_rag/`
- Created fixed chunking implementation in `chunking/fixed_chunking.py`
- Set up vector search foundation in `retrieval/vector_search.py`
- Built simple query processing workflow

## Challenges
- Determining optimal chunk size and overlap for different document types
- Balancing retrieval speed vs. accuracy
- Managing context window limits with large retrieved documents
- Handling edge cases in document preprocessing

## Resources
- LangChain RAG Documentation
- OpenAI Embeddings API
- Research papers on chunking strategies

## Tomorrow's Plan
- Implement ChromaDB integration for vector storage
- Test different persistence configurations
- Benchmark retrieval performance
- Explore advanced ChromaDB features (collections, metadata filtering)
