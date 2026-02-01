"""
Abstract base class for storage backends.

Supports multiple storage options:
- Local filesystem
- Supabase
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class BaseStorage(ABC):
    """
    Abstract storage interface for document and artifact storage.
    
    Implementations should handle:
    - Uploading files (PDFs, embeddings, indices)
    - Downloading files
    - Listing files in a path
    - Deleting files
    """

    @abstractmethod
    def upload(self, local_path: Path, remote_path: str) -> None:
        """
        Upload a file to storage.
        
        Args:
            local_path: Path to local file
            remote_path: Path in storage (e.g., 'chunks/chunks.pkl')
        """
        pass

    @abstractmethod
    def download(self, remote_path: str, local_path: Path) -> None:
        """
        Download a file from storage.
        
        Args:
            remote_path: Path in storage
            local_path: Where to save locally
        """
        pass

    @abstractmethod
    def list_files(self, prefix: str = "") -> List[str]:
        """
        List files in storage with optional prefix.
        
        Args:
            prefix: Optional prefix to filter by (e.g., 'chunks')
            
        Returns:
            List of file paths in storage
        """
        pass

    @abstractmethod
    def delete(self, remote_path: str) -> None:
        """
        Delete a file from storage.
        
        Args:
            remote_path: Path in storage to delete
        """
        pass

    @abstractmethod
    def exists(self, remote_path: str) -> bool:
        """
        Check if a file exists in storage.
        
        Args:
            remote_path: Path in storage
            
        Returns:
            True if file exists
        """
        pass

    @abstractmethod
    def get_url(self, remote_path: str) -> str:
        """
        Get URL or path for a file in storage.
        
        Args:
            remote_path: Path in storage
            
        Returns:
            URL/path to access the file
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
