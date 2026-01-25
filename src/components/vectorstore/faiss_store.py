from typing import List, Dict
from pathlib import Path

import faiss
import numpy as np

from .base import BaseVectorStore


class FAISSVectorStore(BaseVectorStore):
    """FAISS-based vector store implementation."""

    def __init__(self, dimension: int = 384):
        """
        Initialize FAISS vector store.

        Args:
            dimension: Dimension of vectors (default: 384 for MiniLM)
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    def add(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        """Add vectors and metadata to the index."""
        vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Search the index for top_k similar vectors.

        Returns:
            List of dicts with text, metadata, and similarity score
        """
        query_vector = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                "text": self.metadata[idx].get("text", ""),
                "metadata": self.metadata[idx],
                "similarity_score": float(dist)
            })
        return results

    def save(self, path: str) -> None:
        """Save the index and metadata to disk."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "index.faiss"))

        import pickle
        with open(path / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self, path: str) -> None:
        """Load the index and metadata from disk."""
        path = Path(path)
        self.index = faiss.read_index(str(path / "index.faiss"))

        import pickle
        with open(path / "metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)
