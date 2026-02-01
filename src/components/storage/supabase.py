"""
Supabase storage backend.

Stores files in Supabase bucket (cloud storage).
"""

from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv
from .base import BaseStorage
from config import ENV_PATH  # <- use config for .env path


class SupabaseStorage(BaseStorage):
    """
    Supabase storage backend.
    """

    def __init__(self, bucket_name: str):
        """Initialize Supabase storage client."""
        try:
            from supabase import create_client
        except ImportError:
            raise ImportError("supabase-py not installed. Install with `pip install supabase`.")

        # Load .env from config
        load_dotenv(dotenv_path=ENV_PATH)

        # Access only the variables we care about
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials missing. Set SUPABASE_URL and SUPABASE_KEY in .env.")

        self.bucket_name = bucket_name
        self.client = create_client(self.supabase_url, self.supabase_key)

        # Test connection
        try:
            self.client.storage.list_buckets()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Supabase: {e}")

    def upload(self, local_path: Path, remote_path: str) -> None:
        """Upload a file to Supabase bucket."""
        with open(local_path, "rb") as f:
            self.client.storage.from_(self.bucket_name).upload(
                file=f,
                path=remote_path,
                file_options={"cache-control": "3600"}
            )
        print(f"✓ Uploaded to Supabase: {remote_path}")
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
        print(f"\n=== DOWNLOAD CALLED ===")
        print(f"remote_path: {remote_path}")
        print(f"local_path: {local_path}")
        print(f"prefix: '{prefix}'")
        print(f"overwrite: {overwrite}")
        
        # Single file download
        if remote_path is not None:
            print(f"→ SINGLE FILE MODE")
            if local_path is None:
                raise ValueError("local_path required when downloading a specific file")
            
            local_path = Path(local_path)
            print(f"  Target: {local_path.absolute()}")
            
            try:
                print(f"  Calling Supabase API...")
                data = self.client.storage.from_(self.bucket_name).download(remote_path)
                print(f"  ✓ Got data: {len(data)} bytes")
                
                print(f"  Creating parent dir: {local_path.parent.absolute()}")
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                print(f"  Writing to disk...")
                local_path.write_bytes(data)
                
                print(f"  Checking if file exists: {local_path.exists()}")
                if local_path.exists():
                    print(f"  ✓ File size on disk: {local_path.stat().st_size} bytes")
                else:
                    print(f"  ✗ FILE DOES NOT EXIST AFTER WRITE!")
                    
            except Exception as e:
                print(f"  ✗ ERROR: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                raise FileNotFoundError(f"File not found in Supabase: {remote_path}") from e
        
        # Download all files
        else:
            print(f"→ DOWNLOAD ALL MODE")
            if local_path is None:
                raise ValueError("local_path (directory) required when downloading all files")
            
            local_dir = Path(local_path)
            print(f"  Local dir: {local_dir.absolute()}")
            local_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Dir exists: {local_dir.exists()}")
            
            files = self.list_files(prefix=prefix)
            print(f"  Found {len(files)} files: {files}")
            
            if not files:
                print(f"  No files to download")
                return
            
            for i, file_name in enumerate(files, 1):
                print(f"\n  [{i}/{len(files)}] Processing: {file_name}")
                file_local_path = local_dir / file_name
                print(f"       Target path: {file_local_path.absolute()}")
                
                if file_local_path.exists() and not overwrite:
                    print(f"       Skipped (exists)")
                    continue
                
                # Call the single-file version
                self.download(remote_path=file_name, local_path=file_local_path)
    # def download(self, remote_path: str, local_path: Path) -> None:
    #     """Download a file from Supabase bucket."""
    #     try:
    #         data = self.client.storage.from_(self.bucket_name).download(remote_path)
    #         local_path.parent.mkdir(parents=True, exist_ok=True)
    #         local_path.write_bytes(data)
    #         print(f"✓ Downloaded from Supabase: {remote_path}")
    #     except Exception:
    #         raise FileNotFoundError(f"File not found in Supabase: {remote_path}")
            
    # def download_all(self, local_dir: Path, prefix: str = "", overwrite: bool = True) -> None:
    #     """
    #     Download all files from the bucket to a local directory.

    #     Args:
    #         local_dir: Local directory to save files
    #         prefix: Optional prefix to filter files in the bucket
    #         overwrite: Whether to overwrite existing files
    #     """
    #     local_dir = Path(local_dir)
    #     local_dir.mkdir(parents=True, exist_ok=True)

    #     files = self.list_files(prefix=prefix)
    #     if not files:
    #         return

    #     for file_name in files:
    #         local_path = local_dir / Path(file_name).name
    #         if local_path.exists() and not overwrite:
    #             continue
    #         self.download(file_name, local_path)

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in bucket, optionally filtered by prefix."""
        try:
            all_files = self.client.storage.from_(self.bucket_name).list()
            files = [item["name"] for item in all_files if item.get("name")]
            if prefix:
                files = [f for f in files if f.startswith(prefix)]
            return files
        except Exception as e:
            print(f"Warning: Could not list files (prefix='{prefix}'): {e}")
            return []

    def delete(self, remote_path: str) -> None:
        """Delete a file from Supabase bucket."""
        try:
            self.client.storage.from_(self.bucket_name).remove([remote_path])
            print(f"✓ Deleted from Supabase: {remote_path}")
        except Exception as e:
            print(f"Warning: Could not delete {remote_path}: {e}")

    def exists(self, remote_path: str) -> bool:
        """Check if a file exists in bucket."""
        return remote_path in self.list_files(prefix=remote_path)

    def get_url(self, remote_path: str) -> str:
        """Get public URL for a file in bucket."""
        try:
            return self.client.storage.from_(self.bucket_name).get_public_url(remote_path)
        except Exception:
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{remote_path}"

    def __repr__(self) -> str:
        return f"SupabaseStorage(bucket='{self.bucket_name}')"
