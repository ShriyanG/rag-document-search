#!/usr/bin/env python3
"""
Test script: CloudStorage + PDFDataSource
"""

import sys
from pathlib import Path
import shutil

from components.storage.supabase import SupabaseStorage
from components.data.pdf import PDFDataSource

def main():
    print("\n🌥️ Testing CloudStorage PDF Loading\n")

    # Clean the test directory before starting
    BASE_DIR = Path(__file__).parent.parent.parent
    TEST_PDF_DIR = BASE_DIR / "tests/test_data"
    if TEST_PDF_DIR.exists():
        shutil.rmtree(TEST_PDF_DIR)
    TEST_PDF_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Test download directory cleaned: {TEST_PDF_DIR.resolve()}")
    print("Contents now:", list(TEST_PDF_DIR.iterdir()))

    # Create cloud storage instance
    supabase = SupabaseStorage(bucket_name="llm_storage")

    print("\n1. Listing PDFs in cloud storage...")
    pdf_files = supabase.list_files(prefix="")
    print("PDF files found in bucket:", pdf_files)
    if not pdf_files:
        print("   ⚠️ No PDFs found. Check bucket or prefix.")
        return

    print(f"   ✓ Found {len(pdf_files)} PDF(s):")
    for f in pdf_files:
        print(f"     - {f}")

    print("\n2. Downloading PDFs to test directory...")
    # for pdf_file in pdf_files:
    #     local_path = TEST_PDF_DIR / Path(pdf_file).name
    #     supabase.download(pdf_file, local_path)
    supabase.download(
    remote_path=None,
    local_path=Path("tests/test_data"),
    prefix="",
    overwrite=True
)

    # Verify files downloaded
    downloaded_files = list(TEST_PDF_DIR.iterdir())
    print(f"   ✓ Downloaded {len(downloaded_files)} file(s) to {TEST_PDF_DIR}")
    for f in downloaded_files:
        print(f"     - {f.name}")

    print("\n3. Loading PDFs via PDFDataSource...")
    pdf_source = PDFDataSource(
        pdf_dir=TEST_PDF_DIR
    )

    pages = pdf_source.load()
    print(f"   ✓ Loaded {len(pages)} total pages")

    if pages:
        print("\n4. Sample extracted page:")
        print(f"   Page #: {pages[0]['page_number']}")
        print(f"   Text preview:\n{pages[0]['text'][:300]}")

    print("\n✅ Cloud PDF loading test complete!")

if __name__ == "__main__":
    main()
