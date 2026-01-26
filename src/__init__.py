"""
RAG Document Search - Retrieval Augmented Generation pipeline for document analysis
"""

__version__ = "0.1.0"

# Main components
from .rag import run_rag_pipeline, format_context, create_prompt
from .retrieval import retrieve
from .components import (
    BaseLLM, LocalLLM, OpenAILLM,
    BaseVectorStore, FAISSVectorStore,
    BaseDataSource, PDFDataSource
)

__all__ = [
    "run_rag_pipeline",
    "format_context",
    "create_prompt",
    "retrieve",
    "BaseLLM",
    "LocalLLM",
    "OpenAILLM",
    "BaseVectorStore",
    "FAISSVectorStore",
    "BaseDataSource",
    "PDFDataSource",
]
