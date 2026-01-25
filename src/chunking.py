import pickle
from pathlib import Path
from config import PROCESSED_DIR, CHUNK_SIZE, CHUNK_OVERLAP 
from utils import load_pickle, save_pickle

# Helper Functions
def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def chunk_pdf_page_data(page_data, filename):
    """
    Convert page-level data into chunks with metadata.
    """
    all_chunks = []

    for page in page_data:
        page_number = page["page_number"]
        text = page["text"]
        page_chunks = chunk_text(text)
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


# Main Processing Function
def process_all_pickles():
    """
    Load all pickled PDFs in PROCESSED_DIR/pickle/ and generate chunks.
    Save all chunks in PROCESSED_DIR/chunks/
    """
    pickle_dir = PROCESSED_DIR / "pickle"
    chunks_dir = PROCESSED_DIR / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)  # Create folder if not exists

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


# Entry Point
if __name__ == "__main__":
    process_all_pickles()
