import pickle
from pathlib import Path
from config import PROCESSED_DIR, CHUNK_SIZE, CHUNK_OVERLAP  # import from config

# Helper Functions
def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # Move start with overlap
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
        with open(pkl_file, "rb") as f:
            page_data = pickle.load(f)
        chunks = chunk_pdf_page_data(page_data, pkl_file.stem)
        all_chunks.extend(chunks)

    # Save all chunks to a single pickle in chunks folder
    output_file = chunks_dir / "chunks.pkl"
    with open(output_file, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Chunks saved to {output_file}")


# Entry Point
if __name__ == "__main__":
    process_all_pickles()
