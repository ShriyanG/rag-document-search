from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np

from config import EMBEDDINGS_DIR, PROCESSED_DIR
from utils import load_pickle

INDEX_PATH = PROCESSED_DIR / "vector_index.index"


def load_embeddings() -> List[Dict]:
    """Load embedded chunks from disk."""
    return load_pickle(EMBEDDINGS_DIR, "embeddings.pkl")

def build_faiss_index(embedded_chunks: List[Dict]) -> faiss.IndexFlatL2:
    """
    Create a FAISS index from embeddings.
    """
    dimension = embedded_chunks[0]["embedding"].shape[0]
    index = faiss.IndexFlatL2(dimension)  # L2 distance
    vectors = np.array([chunk["embedding"] for chunk in embedded_chunks])
    index.add(vectors)
    return index


def save_index(index: faiss.IndexFlatL2, path: Path = INDEX_PATH) -> None:
    """Persist FAISS index to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(path))


def load_index(path: Path = INDEX_PATH) -> faiss.IndexFlatL2:
    """Load FAISS index from disk."""
    return faiss.read_index(str(path))


def query_index(
    query_vector: np.ndarray,
    index: faiss.IndexFlatL2,
    embedded_chunks: List[Dict],
    top_k: int = 5
) -> List[Dict]:
    """
    Search FAISS index for the top_k most similar chunks.
    Returns list of dicts with 'text' and 'metadata'.
    """
    query_vector = np.array([query_vector]).astype(np.float32)
    distances, indices = index.search(query_vector, top_k)
    results = []
    for idx in indices[0]:
        results.append(embedded_chunks[idx])
    return results


def run_vector_store_pipeline(top_k: int = 5) -> Tuple[faiss.IndexFlatL2, List[Dict]]:
    """
    Build index and return it along with the loaded embeddings.
    """
    embedded_chunks = load_embeddings()
    index = build_faiss_index(embedded_chunks)
    save_index(index)
    return index, embedded_chunks


if __name__ == "__main__":
    # Build and save index for the first time
    print("Building FAISS index...")
    idx, chunks = run_vector_store_pipeline()
    print(f"FAISS index built with {len(chunks)} vectors.")
