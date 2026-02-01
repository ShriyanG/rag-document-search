"""
Supabase storage backend.

Stores files in Supabase bucket (cloud storage).
"""

from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv
from .base import BaseStorage
from config import ENV_PATH


class SupabaseStorage(BaseStorage):
    """
    Supabase storage backend.
    """

    def __init__(self):
        """Initialize Supabase storage client."""
        try:
            from supabase import create_client
        except ImportError:
            raise ImportError("supabase-py not installed. Install with `pip install supabase`.")

        load_dotenv(dotenv_path=ENV_PATH)

        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase_bucket = os.getenv("SUPABASE_BUCKET")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials missing. Set SUPABASE_URL and SUPABASE_KEY in .env.")

        self.client = create_client(self.supabase_url, self.supabase_key)

        try:
            self.client.storage.list_buckets()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Supabase: {e}")

    def upload(self, local_path: Path, remote_path: str) -> None:
        """Upload a file to Supabase bucket."""
        with open(local_path, "rb") as f:
            self.client.storage.from_(self.supabase_bucket).upload(
                file=f,
                path=remote_path,
                file_options={"cache-control": "3600"}
            )

    def download(
        self, 
        remote_path: str | None = None, 
        local_path: Path | None = None,
        prefix: str = "",
        overwrite: bool = True
    ) -> None:
        """
        Download file(s) from Supabase bucket.
        
        Args:
            remote_path: Specific file to download. If None, downloads all files.
            local_path: Local path for single file, or directory for multiple files.
            prefix: Filter files by prefix (only used when downloading all).
            overwrite: Whether to overwrite existing files (only used when downloading all).
        """
        # Single file download
        if remote_path is not None:
            if local_path is None:
                raise ValueError("local_path required when downloading a specific file")
            
            local_path = Path(local_path)
            try:
                data = self.client.storage.from_(self.supabase_bucket).download(remote_path)
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_bytes(data)
            except Exception as e:
                raise FileNotFoundError(f"File not found in Supabase: {remote_path}") from e
        
        # Download all files
        else:
            if local_path is None:
                raise ValueError("local_path (directory) required when downloading all files")
            
            local_dir = Path(local_path)
            local_dir.mkdir(parents=True, exist_ok=True)
            
            files = self.list_files(prefix=prefix)
            if not files:
                return
            
            for file_name in files:
                file_local_path = local_dir / file_name
                
                if file_local_path.exists() and not overwrite:
                    continue
                
                # Call the single-file version
                self.download(remote_path=file_name, local_path=file_local_path)

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in bucket, optionally filtered by prefix."""
        try:
            all_files = self.client.storage.from_(self.bucket_name).list()
            files = [item["name"] for item in all_files if item.get("name")]
            if prefix:
                files = [f for f in files if f.startswith(prefix)]
            return files
        except Exception:
            return []

    def delete(self, remote_path: str) -> None:
        """Delete a file from Supabase bucket."""
        try:
            self.client.storage.from_(self.bucket_name).remove([remote_path])
        except Exception:
            pass

    def exists(self, remote_path: str) -> bool:
        """Check if a file exists in bucket."""
        return remote_path in self.list_files(prefix=remote_path)

    def get_url(self, remote_path: str) -> str:
        """Get public URL for a file in bucket."""
        try:
            return self.client.storage.from_(self.supabase_bucket).get_public_url(remote_path)
        except Exception:
            return f"{self.supabase_url}/storage/v1/object/public/{self.supabase_bucket}/{remote_path}"

    def __repr__(self) -> str:
        return f"SupabaseStorage(bucket='{self.supabase_bucket}')"