#!/usr/bin/env python3
"""
Test script: CloudStorage + PDFDataSource
"""

from pathlib import Path
import shutil

from components.storage.supabase import SupabaseStorage
from components.data.pdf import PDFDataSource


def main():
    # Setup test directory
    TEST_PDF_DIR = Path("tests/test_data")
    
    if TEST_PDF_DIR.exists():
        shutil.rmtree(TEST_PDF_DIR)
    TEST_PDF_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize cloud storage and list files
    supabase = SupabaseStorage(bucket_name="llm_storage")
    pdf_files = supabase.list_files(prefix="")
    
    if not pdf_files:
        print("⚠️  No files found in bucket")
        return

    # Download all files
    supabase.download(
        remote_path=None,
        local_path=TEST_PDF_DIR,
        prefix="",
        overwrite=True
    )

    # Load PDFs
    pdf_source = PDFDataSource(pdf_dir=TEST_PDF_DIR)
    pages = pdf_source.load()
    
    # Show results
    if pages:
        print(f"\n✓ Loaded {len(pages)} pages from {len(pdf_files)} file(s)")
        print(f"Sample: {pages[0]['text'][:200]}...")
    else:
        print("⚠️  No pages loaded")


if __name__ == "__main__":
    main()