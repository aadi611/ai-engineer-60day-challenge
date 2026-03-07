"""
Example Usage of the RAG System
Demonstrates basic functionality
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pipeline import RAGPipeline
from src.document_loader import Document
import tempfile
import os


def create_sample_documents():
    """Create sample documents for testing"""
    temp_dir = tempfile.mkdtemp()
    
    # Sample document 1
    doc1_content = """
    Machine Learning and Artificial Intelligence
    
    Machine learning is a subset of artificial intelligence (AI) that focuses on enabling 
    computers to learn from data without being explicitly programmed. It uses algorithms 
    that iteratively learn from data to improve predictions or decisions.
    
    Types of Machine Learning:
    1. Supervised Learning: Learning from labeled data
    2. Unsupervised Learning: Finding patterns in unlabeled data
    3. Reinforcement Learning: Learning through trial and error
    """
    
    doc1_path = Path(temp_dir) / "ml_basics.txt"
    with open(doc1_path, 'w') as f:
        f.write(doc1_content)
    
    # Sample document 2
    doc2_content = """
    Deep Learning and Neural Networks
    
    Deep learning is a specialized subset of machine learning that uses neural networks 
    with multiple layers (deep neural networks). These networks can automatically learn 
    hierarchical representations of data.
    
    Key Concepts:
    - Neural Networks: Computational models inspired by the human brain
    - Backpropagation: Algorithm for training neural networks
    - Activation Functions: Functions that introduce non-linearity
    - Convolutional Neural Networks (CNNs): Specialized for image processing
    - Recurrent Neural Networks (RNNs): Specialized for sequential data
    """
    
    doc2_path = Path(temp_dir) / "deep_learning.txt"
    with open(doc2_path, 'w') as f:
        f.write(doc2_content)
    
    # Sample document 3
    doc3_content = """
    RAG: Retrieval-Augmented Generation
    
    Retrieval-Augmented Generation (RAG) is a technique that enhances large language models 
    by combining them with information retrieval systems. RAG allows models to access 
    external knowledge bases, making their responses more accurate and up-to-date.
    
    How RAG Works:
    1. User submits a query
    2. System retrieves relevant documents from a knowledge base
    3. Retrieved documents are used as context
    4. LLM generates a response based on the query and context
    5. Response is grounded in the retrieved information
    
    Benefits of RAG:
    - Reduces hallucinations by grounding responses in facts
    - Allows for up-to-date information without retraining
    - More cost-effective than fine-tuning for specific domains
    """
    
    doc3_path = Path(temp_dir) / "rag_explained.txt"
    with open(doc3_path, 'w') as f:
        f.write(doc3_content)
    
    return temp_dir, [doc1_path, doc2_path, doc3_path]


def main():
    """Main example script"""
    print("=" * 60)
    print("RAG System - Example Usage")
    print("=" * 60)
    print()
    
    # Create sample documents
    print("📄 Creating sample documents...")
    temp_dir, doc_paths = create_sample_documents()
    print(f"✓ Created {len(doc_paths)} sample documents")
    print()
    
    # Initialize pipeline
    print("🚀 Initializing RAG pipeline...")
    pipeline = RAGPipeline()
    print("✓ Pipeline initialized")
    print()
    
    # Show initial stats
    print("📊 Initial System Stats:")
    stats = pipeline.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Ingest documents
    print("📚 Ingesting documents...")
    count = pipeline.ingest_documents(file_paths=[str(p) for p in doc_paths])
    print(f"✓ Ingested {count} documents")
    print()
    
    # Show updated stats
    print("📊 Updated System Stats:")
    stats = pipeline.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Example queries
    queries = [
        "What is machine learning?",
        "Explain deep learning and neural networks",
        "How does RAG work?",
        "What are the types of machine learning?"
    ]
    
    print("=" * 60)
    print("Running Example Queries")
    print("=" * 60)
    print()
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Query {i}: {query}")
        print("=" * 60)
        
        # Query the system
        result = pipeline.query(query)
        
        # Display response
        print("\n📝 Response:")
        print(result["response"])
        
        # Display sources
        if result.get("sources"):
            print(f"\n📚 Sources ({len(result['sources'])}):")
            for source in result["sources"]:
                metadata = source.get("metadata", {})
                source_name = metadata.get("file_name", "Unknown")
                score = source.get("score", 0.0)
                print(f"   [{source['source_number']}] {source_name} (score: {score:.3f})")
        
        print()
    
    # Cleanup
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print()
    print("To clean up temporary files:")
    print(f"   rm -rf {temp_dir}")
    print()
    print("To run the interactive chatbot:")
    print("   python chatbot.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
