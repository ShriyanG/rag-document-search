from abc import ABC, abstractmethod
from typing import List, Dict
from pathlib import Path


class BaseDataSource(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    def load(self) -> List[Dict]:
        """
        Load and return documents/pages.

        Returns:
            List of dicts with 'text' and metadata
        """
        pass

    @abstractmethod
    def process(self, save_txt: bool = False) -> None:
        """
        Process and ingest the data source.

        Args:
            save_txt: Whether to save human-readable text files
        """
        pass
