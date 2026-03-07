"""
RAG Pipeline
Main orchestration of the RAG system components
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import yaml
from loguru import logger
from dotenv import load_dotenv
import os

# Robustly find and load the .env file from the project root (Projects/RAG/)
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(dotenv_path=_ENV_PATH, override=True)
    logger.debug(f".env loaded from: {_ENV_PATH}")
else:
    logger.warning(f".env file NOT found at: {_ENV_PATH}")

from .document_loader import DocumentLoader, Document, preprocess_text
from .chunking import FixedSizeChunker, RecursiveChunker, SemanticChunker
from .embeddings import EmbeddingGenerator
from .storage import ChromaStore
from .retrieval.vector_retriever import VectorRetriever
from .retrieval.bm25_retriever import BM25Retriever
from .retrieval.hybrid_retriever import HybridRetriever
from .retrieval.reranker import Reranker
from .generation import LLMGenerator


class RAGPipeline:
    """
    Production-grade RAG Pipeline
    Orchestrates document loading, chunking, retrieval, and generation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize RAG pipeline
        
        Args:
            config_path: Path to configuration file
        """
        # Load environment variables
        load_dotenv(dotenv_path=_ENV_PATH, override=True)
        
        # Load configuration
        if config_path:
            self.config = self._load_config(config_path)
        else:
            self.config = self._default_config()
        
        # Initialize components
        self._initialize_components()
        
        # Document cache for BM25
        self._document_cache = []
        
        logger.info("RAGPipeline initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from: {config_path}")
        return config
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "chunking": {
                "strategy": "recursive",
                "chunk_size": 500,
                "chunk_overlap": 50
            },
            "embeddings": {
                "model": "text-embedding-3-small"
            },
            "vector_store": {
                "collection_name": "rag_documents",
                "persist_directory": "./data/chroma_db",
                "distance_metric": "cosine"
            },
            "retrieval": {
                "strategy": "hybrid",
                "top_k": 10
            },
            "reranking": {
                "enabled": True,
                "top_k": 5
            },
            "llm": {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }
    
    def _initialize_components(self):
        """Initialize all pipeline components"""
        # Re-load .env explicitly here to guarantee vars are in os.environ
        load_dotenv(dotenv_path=_ENV_PATH, override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Fallback: read the file directly if os.getenv still returns None
        if not api_key and _ENV_PATH.exists():
            from dotenv import dotenv_values
            env_vals = dotenv_values(_ENV_PATH)
            api_key = env_vals.get("OPENAI_API_KEY")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                logger.debug("API key loaded via dotenv_values fallback")
        
        if not api_key:
            raise EnvironmentError(
                f"OPENAI_API_KEY not found in environment or {_ENV_PATH}\n"
                f"Make sure .env contains: OPENAI_API_KEY=sk-..."
            )
        
        # Document loader
        self.doc_loader = DocumentLoader()
        
        # Chunker
        chunking_config = self.config["chunking"]
        strategy = chunking_config.get("strategy", "recursive")
        
        if strategy == "fixed":
            self.chunker = FixedSizeChunker(
                chunk_size=chunking_config.get("chunk_size", 500),
                chunk_overlap=chunking_config.get("chunk_overlap", 50)
            )
        elif strategy == "semantic":
            self.chunker = SemanticChunker(
                chunk_size=chunking_config.get("chunk_size", 500),
                chunk_overlap=chunking_config.get("chunk_overlap", 50)
            )
        else:  # recursive
            self.chunker = RecursiveChunker(
                chunk_size=chunking_config.get("chunk_size", 500),
                chunk_overlap=chunking_config.get("chunk_overlap", 50)
            )
        
        # Embedding generator
        embedding_config = self.config["embeddings"]
        self.embedding_generator = EmbeddingGenerator(
            model=embedding_config.get("model", "text-embedding-3-small"),
            api_key=api_key
        )
        
        # Vector store
        store_config = self.config["vector_store"]
        self.vector_store = ChromaStore(
            collection_name=store_config.get("collection_name", "rag_documents"),
            persist_directory=store_config.get("persist_directory", "./data/chroma_db"),
            distance_metric=store_config.get("distance_metric", "cosine")
        )
        
        # Vector retriever
        self.vector_retriever = VectorRetriever(
            store=self.vector_store,
            embedding_generator=self.embedding_generator,
            top_k=self.config["retrieval"].get("top_k", 10)
        )
        
        # BM25 retriever (will be initialized when adding documents)
        self.bm25_retriever = None
        
        # Reranker
        rerank_config = self.config.get("reranking", {})
        if rerank_config.get("enabled", False):
            try:
                self.reranker = Reranker(
                    top_k=rerank_config.get("top_k", 5)
                )
            except Exception as e:
                logger.warning(f"Failed to load reranker: {e}")
                self.reranker = None
        else:
            self.reranker = None
        
        # LLM generator
        llm_config = self.config["llm"]
        self.llm_generator = LLMGenerator(
            model=llm_config.get("model", "gpt-4-turbo-preview"),
            api_key=api_key,
            temperature=llm_config.get("temperature", 0.7),
            max_tokens=llm_config.get("max_tokens", 1000)
        )
        
        logger.info("All components initialized")
    
    def ingest_documents(
        self,
        file_paths: Optional[List[str]] = None,
        directory_path: Optional[str] = None
    ) -> int:
        """
        Ingest documents into the RAG system
        
        Args:
            file_paths: List of file paths to ingest
            directory_path: Directory containing documents to ingest
            
        Returns:
            Number of documents ingested
        """
        documents = []
        
        # Load documents
        if file_paths:
            for file_path in file_paths:
                try:
                    doc = self.doc_loader.load(file_path)
                    documents.append(doc)
                except Exception as e:
                    logger.error(f"Failed to load {file_path}: {e}")
        
        if directory_path:
            try:
                dir_docs = self.doc_loader.load_directory(directory_path)
                documents.extend(dir_docs)
            except Exception as e:
                logger.error(f"Failed to load directory {directory_path}: {e}")
        
        if not documents:
            logger.warning("No documents to ingest")
            return 0
        
        # Process documents
        all_chunks = []
        for doc in documents:
            # Preprocess
            cleaned_text = preprocess_text(doc.content)
            
            # Chunk
            chunks = self.chunker.chunk(cleaned_text, metadata=doc.metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        
        # Generate embeddings
        chunk_contents = [chunk.content for chunk in all_chunks]
        embeddings = self.embedding_generator.embed(chunk_contents)
        
        # Store in vector database
        self.vector_store.add_chunks(all_chunks, embeddings)
        
        # Update document cache for BM25
        for chunk in all_chunks:
            self._document_cache.append({
                "id": chunk.chunk_id,
                "content": chunk.content,
                "metadata": chunk.metadata
            })
        
        # Initialize/update BM25 retriever
        self._initialize_bm25()
        
        logger.success(f"Successfully ingested {len(documents)} documents, {len(all_chunks)} chunks")
        return len(documents)
    
    def _initialize_bm25(self):
        """Initialize or update BM25 retriever"""
        if self._document_cache:
            retrieval_config = self.config["retrieval"]
            self.bm25_retriever = BM25Retriever(
                documents=self._document_cache,
                top_k=retrieval_config.get("top_k", 10)
            )
            logger.info("BM25 retriever initialized")
    
    def query(
        self,
        query: str,
        retrieval_strategy: Optional[str] = None,
        top_k: Optional[int] = None,
        include_citations: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            query: User query
            retrieval_strategy: 'vector', 'bm25', or 'hybrid' (default: from config)
            top_k: Number of documents to retrieve
            include_citations: Whether to include source citations
            
        Returns:
            Response dictionary with answer and sources
        """
        if not query or not query.strip():
            return {
                "response": "Please provide a valid query.",
                "sources": [],
                "error": "Empty query"
            }
        
        logger.info(f"Processing query: {query[:100]}...")
        
        # Determine retrieval strategy
        strategy = retrieval_strategy or self.config["retrieval"].get("strategy", "hybrid")
        k = top_k or self.config["retrieval"].get("top_k", 10)
        
        # Retrieve documents
        if strategy == "vector":
            retrieved_docs = self.vector_retriever.retrieve(query, top_k=k)
        elif strategy == "bm25":
            if not self.bm25_retriever:
                logger.warning("BM25 not initialized, falling back to vector")
                retrieved_docs = self.vector_retriever.retrieve(query, top_k=k)
            else:
                retrieved_docs = self.bm25_retriever.retrieve(query, top_k=k)
        else:  # hybrid
            if not self.bm25_retriever:
                logger.warning("BM25 not initialized, using vector only")
                retrieved_docs = self.vector_retriever.retrieve(query, top_k=k)
            else:
                hybrid_retriever = HybridRetriever(
                    vector_retriever=self.vector_retriever,
                    bm25_retriever=self.bm25_retriever,
                    fusion_method=self.config["retrieval"].get("hybrid", {}).get("fusion_method", "rrf"),
                    alpha=self.config["retrieval"].get("hybrid", {}).get("alpha", 0.5),
                    top_k=k
                )
                retrieved_docs = hybrid_retriever.retrieve(query)
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        
        # Rerank if enabled
        if self.reranker and retrieved_docs:
            rerank_k = self.config.get("reranking", {}).get("top_k", 5)
            retrieved_docs = self.reranker.rerank(query, retrieved_docs, top_k=rerank_k)
            logger.info(f"Reranked to top {len(retrieved_docs)} documents")
        
        # Generate response
        result = self.llm_generator.generate(
            query=query,
            retrieved_docs=retrieved_docs,
            include_citations=include_citations
        )
        
        logger.success("Query processed successfully")
        return result
    
    def reset(self):
        """Reset the RAG system (clear all documents)"""
        self.vector_store.reset()
        self._document_cache = []
        self.bm25_retriever = None
        logger.warning("RAG system reset - all documents cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "total_chunks": self.vector_store.count(),
            "collections": self.vector_store.list_collections(),
            "chunking_strategy": self.config["chunking"]["strategy"],
            "retrieval_strategy": self.config["retrieval"]["strategy"],
            "reranking_enabled": self.config.get("reranking", {}).get("enabled", False)
        }


if __name__ == "__main__":
    # Test the pipeline
    pipeline = RAGPipeline()
    print("RAG Pipeline initialized")
    print(f"Stats: {pipeline.get_stats()}")
