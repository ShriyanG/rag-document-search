#!/usr/bin/env python3
"""
RAG Document Search - Main entry point
"""

import argparse
from pathlib import Path

from rag import run_rag_pipeline
from components.data.pdf import process_all_pdfs
from retrieval.embeddings import run_embedding_pipeline
from retrieval.indexing import run_vector_store_pipeline


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


def query_pipeline(query: str, top_k: int = 5):
    """
    Run a single query through the RAG pipeline.
    
    Args:
        query: The question to answer
        top_k: Number of documents to retrieve
    """
    print(f"Query: {query}\n")
    answer = run_rag_pipeline(query, top_k=top_k, max_tokens=250)
    print(f"Answer:\n{answer}\n")


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
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_pipeline(
            skip_ingestion=args.skip_ingestion,
            skip_embedding=args.skip_embedding,
            skip_indexing=args.skip_indexing
        )
    elif args.command == "query":
        query_pipeline(args.query, top_k=args.top_k)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
