from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL_NAME, EMBEDDINGS_DIR
from utils import load_pickle
from .search import search_index, embed_query
from .indexing import load_faiss_index


# Global cache for performance
_cached_model = None
_cached_index = None
_cached_embeddings = None


def get_cached_model():
    """Get or load the embedding model (cached for performance)"""
    global _cached_model
    if _cached_model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
        _cached_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("✓ Embedding model loaded")
    return _cached_model


def get_cached_index():
    """Get or load the FAISS index (cached for performance)"""
    global _cached_index
    if _cached_index is None:
        print("Loading FAISS index...")
        _cached_index = load_faiss_index()
        print("✓ FAISS index loaded")
    return _cached_index


def get_cached_embeddings():
    """Get or load the embeddings (cached for performance)"""
    global _cached_embeddings
    if _cached_embeddings is None:
        print("Loading embeddings...")
        _cached_embeddings = load_pickle(EMBEDDINGS_DIR, "embeddings.pkl")
        print(f"✓ Loaded {len(_cached_embeddings)} embeddings")
    return _cached_embeddings


def retrieve(
    query: str,
    top_k: int = 5
) -> List[Dict]:
    """
    High-level retrieval function:
    - Load embeddings (cached)
    - Load FAISS index (cached)
    - Embed query
    - Search index
    - Return ranked results
    """
    embedded_chunks = get_cached_embeddings()
    index = get_cached_index()
    model = get_cached_model()
    query_vector = embed_query(query, model)
    results = search_index(query_vector, index, embedded_chunks, top_k)
    return results


if __name__ == "__main__":
    # Simple test run
    results = retrieve(
        query="What is the main topic of this document?",
        top_k=3
    )

    for r in results:
        print("-" * 40)
        print(r["metadata"])
        print(r["text"][:300])
