from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL_NAME, EMBEDDINGS_DIR
from utils import load_pickle
from .search import search_index, embed_query
from .indexing import load_faiss_index


def retrieve(
    query: str,
    top_k: int = 5
) -> List[Dict]:
    """
    High-level retrieval function:
    - Load embeddings
    - Load FAISS index
    - Embed query
    - Search index
    - Return ranked results
    """
    embedded_chunks = load_pickle(EMBEDDINGS_DIR, "embeddings.pkl")
    index = load_faiss_index()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
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
