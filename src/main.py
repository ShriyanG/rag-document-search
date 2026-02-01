#!/usr/bin/env python3
"""
RAG Document Search - Main entry point
"""

import argparse
from pathlib import Path

from rag import run_rag_pipeline
from rag.pipeline import set_llm
from components.llm import LLMFactory
from components.data.pdf import process_all_pdfs
from retrieval.embeddings import run_embedding_pipeline
from retrieval.indexing import run_vector_store_pipeline
from config.settings import DEFAULT_LLM_MODEL


def setup_pipeline(skip_ingestion=False, skip_embedding=False, skip_indexing=False):
    """
    Set up the complete pipeline.
    
    Steps:
    1. Ingest PDFs and extract text
    2. Generate embeddings
    3. Build FAISS index
    """
    if not skip_ingestion:
        print("Step 1: Ingesting PDFs...")
        process_all_pdfs(save_txt=True)
        print("✓ PDF ingestion complete\n")
    
    if not skip_embedding:
        print("Step 2: Generating embeddings...")
        run_embedding_pipeline()
        print("✓ Embeddings generated\n")
    
    if not skip_indexing:
        print("Step 3: Building FAISS index...")
        idx, chunks = run_vector_store_pipeline()
        print(f"✓ Index built with {len(chunks)} vectors\n")


def query_pipeline(query: str, top_k: int = 5, llm_model: str = None):
    """
    Run a single query through the RAG pipeline.
    
    Args:
        query: The question to answer
        top_k: Number of documents to retrieve
        llm_model: LLM model to use
    """
    if llm_model:
        print(f"Using LLM: {llm_model}\n")
        set_llm(llm_model)
    
    print(f"Query: {query}\n")
    answer = run_rag_pipeline(query, top_k=top_k)
    print(f"Answer:\n{answer}\n")


def list_llms():
    """List all supported LLM models."""
    models = LLMFactory.list_models()
    print("\n📚 Supported LLM Models:\n")
    for provider, model_list in models.items():
        print(f"  {provider.upper()}:")
        for model in model_list:
            print(f"    - {model}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="RAG Document Search - Retrieval Augmented Generation Pipeline"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up the RAG pipeline")
    setup_parser.add_argument("--skip-ingestion", action="store_true", help="Skip PDF ingestion")
    setup_parser.add_argument("--skip-embedding", action="store_true", help="Skip embedding generation")
    setup_parser.add_argument("--skip-indexing", action="store_true", help="Skip index building")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG pipeline")
    query_parser.add_argument("query", type=str, help="Question to answer")
    query_parser.add_argument("--top-k", type=int, default=5, help="Number of documents to retrieve")
    query_parser.add_argument(
        "--llm",
        type=str,
        default=None,
        help=f"LLM model to use (default: {DEFAULT_LLM_MODEL})"
    )
    
    # List models command
    list_parser = subparsers.add_parser("list-llms", help="List all supported LLM models")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_pipeline(
            skip_ingestion=args.skip_ingestion,
            skip_embedding=args.skip_embedding,
            skip_indexing=args.skip_indexing
        )
    elif args.command == "query":
        query_pipeline(args.query, top_k=args.top_k, llm_model=args.llm)
    elif args.command == "list-llms":
        list_llms()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
