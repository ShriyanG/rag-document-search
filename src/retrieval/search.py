from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    """
    Convert a user query into an embedding vector.
    """
    query_vector = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return query_vector


def search_index(
    query_vectors: np.ndarray,          # Can be 1D (single query) or 2D (multiple queries)
    index: faiss.Index,
    embedded_chunks: List[Dict],
    top_k: int = 5
) -> List[List[Dict]]:
    """
    Search the FAISS index and return top_k matching chunks
    with text, metadata, and similarity score.

    Returns:
        A list of lists of dictionaries:
            - Outer list: one entry per query
            - Inner list: top_k results for that query
    """
    # Ensure query_vectors is 2D
    if query_vectors.ndim == 1:
        query_vectors = np.array([query_vectors], dtype=np.float32)
    else:
        query_vectors = query_vectors.astype(np.float32)

    distances, indices = index.search(query_vectors, top_k)
    all_results = []

    # Loop over each query row
    for row_indices, row_distances in zip(indices, distances):
        query_results = []
        for dist, idx in zip(row_distances, row_indices):
            chunk = embedded_chunks[idx]
            query_results.append({
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "similarity_score": float(dist)
            })
        all_results.append(query_results)

    # If only 1 query, return just the inner list for convenience
    if all_results and len(all_results) == 1:
        return all_results[0]
    return all_results
