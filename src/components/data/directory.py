"""
Data processing utilities for chunking and organizing data.
"""

from typing import List, Dict
from pathlib import Path

from config import PROCESSED_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from utils import load_pickle, save_pickle, chunk_text


def chunk_pdf_page_data(page_data: List[Dict], filename: str) -> List[Dict]:
    """
    Convert page-level data into chunks with metadata.

    Args:
        page_data: List of dicts with page number and text
        filename: Source filename for metadata

    Returns:
        List of chunked data with metadata
    """
    all_chunks = []

    for page in page_data:
        page_number = page["page_number"]
        text = page["text"]
        page_chunks = chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        for i, chunk in enumerate(page_chunks, start=1):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "filename": filename,
                    "page_number": page_number,
                    "chunk_id": i
                }
            })
    return all_chunks


def process_all_pickles() -> None:
    """
    Load all pickled PDFs in PROCESSED_DIR/pickle/ and generate chunks.
    Save all chunks in PROCESSED_DIR/chunks/
    """
    pickle_dir = PROCESSED_DIR / "pickle"
    chunks_dir = PROCESSED_DIR / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    pickle_files = list(pickle_dir.glob("*.pkl"))
    all_chunks = []

    for pkl_file in pickle_files:
        page_data = load_pickle(directory=pickle_dir, filename=pkl_file.name)
        chunks = chunk_pdf_page_data(page_data, pkl_file.stem)
        all_chunks.extend(chunks)

    # Save all chunks to a single pickle in chunks folder
    save_pickle(
        directory=chunks_dir,
        data=all_chunks,
        filename="chunks.pkl"
    )

    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Chunks saved to {chunks_dir / 'chunks.pkl'}")


if __name__ == "__main__":
    process_all_pickles()
