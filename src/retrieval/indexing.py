from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np

from config import EMBEDDINGS_DIR, INDEX_PATH
from utils import load_pickle


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


def load_faiss_index(path: Path = INDEX_PATH) -> faiss.IndexFlatL2:
    """Load FAISS index from disk."""
    if not path.exists():
        raise FileNotFoundError(f"FAISS index not found at {path}")
    return faiss.read_index(str(path))


def run_vector_store_pipeline() -> tuple[faiss.IndexFlatL2, List[Dict]]:
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
