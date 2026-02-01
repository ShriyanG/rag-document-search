"""
Local filesystem storage backend.

Stores files on the local machine.
"""

import shutil
from pathlib import Path
from typing import List
from .base import BaseStorage


class LocalStorage(BaseStorage):
    """
    Local filesystem storage backend.
    
    Stores files in a specified directory on the local machine.
    Useful for testing and development.
    """

    def __init__(self, base_dir: Path):
        """
        Initialize local storage.
        
        Args:
            base_dir: Base directory for storage
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, local_path: Path, remote_path: str) -> None:
        """
        Copy a file to storage directory.
        
        Args:
            local_path: Source file path
            remote_path: Destination path relative to base_dir
        """
        dest = self.base_dir / remote_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local_path, dest)
        print(f"✓ Uploaded: {remote_path}")

    def download(self, remote_path: str, local_path: Path) -> None:
        """
        Copy a file from storage directory.
        
        Args:
            remote_path: Source path in storage
            local_path: Destination file path
        """
        src = self.base_dir / remote_path
        if not src.exists():
            raise FileNotFoundError(f"File not found in storage: {remote_path}")
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, local_path)
        print(f"✓ Downloaded: {remote_path}")

    def list_files(self, prefix: str = "") -> List[str]:
        """
        List all files in storage with optional prefix.
        
        Args:
            prefix: Optional prefix to filter by (e.g., 'chunks')
            
        Returns:
            List of relative paths to files
        """
        path = self.base_dir / prefix if prefix else self.base_dir
        if not path.exists():
            return []
        
        files = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                relative = file_path.relative_to(self.base_dir)
                files.append(str(relative))
        return files

    def delete(self, remote_path: str) -> None:
        """
        Delete a file from storage.
        
        Args:
            remote_path: Path in storage to delete
        """
        file_path = self.base_dir / remote_path
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Deleted: {remote_path}")

    def exists(self, remote_path: str) -> bool:
        """
        Check if a file exists in storage.
        
        Args:
            remote_path: Path in storage
            
        Returns:
            True if file exists
        """
        return (self.base_dir / remote_path).exists()

    def get_url(self, remote_path: str) -> str:
        """
        Get local path to file.
        
        Args:
            remote_path: Path in storage
            
        Returns:
            Absolute local path
        """
        return str(self.base_dir / remote_path)

    def __repr__(self) -> str:
        return f"LocalStorage(base_dir='{self.base_dir}')"
