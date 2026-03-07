"""
RAG System Source Package
"""

__version__ = "1.0.0"

from .document_loader import Document, DocumentLoader, preprocess_text

__all__ = [
    "Document",
    "DocumentLoader",
    "preprocess_text"
]
