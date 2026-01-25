from abc import ABC, abstractmethod
from typing import List, Dict
import numpy as np


class BaseVectorStore(ABC):
    """Abstract base class for vector store implementations."""

    @abstractmethod
    def add(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        """
        Add vectors and their metadata to the store.

        Args:
            vectors: 2D array of vectors to add
            metadata: List of metadata dicts corresponding to vectors
        """
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Search for similar vectors.

        Args:
            query_vector: Query vector to search for
            top_k: Number of results to return

        Returns:
            List of results with vectors, metadata, and scores
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Persist the vector store to disk."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Load the vector store from disk."""
        pass
