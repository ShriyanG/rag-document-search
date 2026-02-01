"""
Supabase storage backend.

Stores files in Supabase bucket (cloud storage).
"""

from pathlib import Path
from typing import List, Optional
import os
from .base import BaseStorage


class SupabaseStorage(BaseStorage):
    """
    Supabase storage backend.
    
    Stores files in a Supabase bucket. Requires supabase-py package.
    Set credentials in environment variables:
    - SUPABASE_URL: Project URL
    - SUPABASE_KEY: Service role key or anon key
    """

    def __init__(
        self,
        bucket_name: str,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None
    ):
        """
        Initialize Supabase storage.
        
        Args:
            bucket_name: Name of the Supabase bucket
            supabase_url: Supabase project URL (uses env var if None)
            supabase_key: Supabase API key (uses env var if None)
            
        Raises:
            ImportError: If supabase not installed
            ValueError: If credentials not provided or found
        """
        try:
            from supabase import create_client
        except ImportError:
            raise ImportError(
                "supabase-py not installed. "
                "Install with: pip install supabase"
            )
        
        # Get credentials from arguments or environment
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase credentials not provided. "
                "Set SUPABASE_URL and SUPABASE_KEY environment variables "
                "or pass them as arguments."
            )
        
        self.bucket_name = bucket_name
        self.client = create_client(self.supabase_url, self.supabase_key)
        
        # Test connection
        try:
            self.client.storage.list_buckets()
        except Exception as e:
            raise ValueError(f"Failed to connect to Supabase: {e}")

    def upload(self, local_path: Path, remote_path: str) -> None:
        """
        Upload a file to Supabase bucket.
        
        Args:
            local_path: Path to local file
            remote_path: Path in bucket (e.g., 'chunks/chunks.pkl')
        """
        with open(local_path, "rb") as f:
            self.client.storage.from_(self.bucket_name).upload(
                file=f,
                path=remote_path,
                file_options={"cache-control": "3600"}
            )
        print(f"✓ Uploaded to Supabase: {remote_path}")

    def download(self, remote_path: str, local_path: Path) -> None:
        """
        Download a file from Supabase bucket.
        
        Args:
            remote_path: Path in bucket
            local_path: Where to save locally
        """
        try:
            response = self.client.storage.from_(self.bucket_name).download(remote_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response)
            print(f"✓ Downloaded from Supabase: {remote_path}")
        except Exception as e:
            raise FileNotFoundError(f"File not found in Supabase: {remote_path}") from e

    def list_files(self, prefix: str = "") -> List[str]:
        """
        List files in bucket with optional prefix.
        
        Args:
            prefix: Optional prefix to filter by (e.g., 'chunks')
            
        Returns:
            List of file paths in bucket
        """
        try:
            response = self.client.storage.from_(self.bucket_name).list(prefix)
            return [item["name"] for item in response if item["name"]]
        except Exception as e:
            print(f"Warning: Could not list files with prefix '{prefix}': {e}")
            return []

    def delete(self, remote_path: str) -> None:
        """
        Delete a file from Supabase bucket.
        
        Args:
            remote_path: Path in bucket to delete
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([remote_path])
            print(f"✓ Deleted from Supabase: {remote_path}")
        except Exception as e:
            print(f"Warning: Could not delete {remote_path}: {e}")

    def exists(self, remote_path: str) -> bool:
        """
        Check if a file exists in bucket.
        
        Args:
            remote_path: Path in bucket
            
        Returns:
            True if file exists
        """
        try:
            files = self.list_files(prefix=remote_path)
            return any(f == remote_path for f in files)
        except Exception:
            return False

    def get_url(self, remote_path: str) -> str:
        """
        Get public URL for a file in bucket.
        
        Args:
            remote_path: Path in bucket
            
        Returns:
            Public URL to the file
        """
        try:
            response = self.client.storage.from_(self.bucket_name).get_public_url(remote_path)
            return response
        except Exception as e:
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{remote_path}"

    def __repr__(self) -> str:
        return f"SupabaseStorage(bucket='{self.bucket_name}')"
