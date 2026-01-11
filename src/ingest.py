# src/ingest.py

import fitz  # PyMuPDF
from pathlib import Path
from config import PDF_DIR, PROCESSED_DIR
import re
import pickle

# ----------------------------
# Helper Functions
# ----------------------------

def clean_text(text: str) -> str:
    """
    Clean extracted text from PDFs.

    Steps:
    - Remove page number patterns like "Page 1 of 5"
    - Flatten whitespace and line breaks
    - Remove non-printable characters
    """
    text = re.sub(r"page \d+ of \d+", "", text, flags=re.IGNORECASE)
    text = " ".join(text.split())
    text = "".join(c for c in text if c.isprintable())
    return text


def extract_text_with_metadata(pdf_path: Path):
    """
    Extract text from each page of a PDF and clean it.

    Returns:
        List of dictionaries with page number and cleaned text
    """
    page_data = []
    with fitz.open(pdf_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            raw_text = page.get_text()
            cleaned_text = clean_text(raw_text)
            if cleaned_text.strip():
                page_data.append({
                    "page_number": page_number,
                    "text": cleaned_text
                })
    return page_data


# ----------------------------
# Main Processing Function
# ----------------------------

def process_all_pdfs(save_txt=True):
    """
    Process all PDFs in PDF_DIR:
    - Save pickled page-level metadata in PROCESSED_DIR/pickle/
    - Optionally save human-readable .txt in PROCESSED_DIR/txt/
    """
    pickle_dir = PROCESSED_DIR / "pickle"
    txt_dir = PROCESSED_DIR / "txt"

    # Create folders if they don't exist
    pickle_dir.mkdir(parents=True, exist_ok=True)
    txt_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF(s) to process.")

    for pdf_file in pdf_files:
        pages = extract_text_with_metadata(pdf_file)

        if pages:
            # Save pickled object
            pickle_file = pickle_dir / f"{pdf_file.stem}.pkl"
            with open(pickle_file, "wb") as f:
                pickle.dump(pages, f)
            print(f"Pickled: {pickle_file.name}")

            # Optionally save human-readable text file
            if save_txt:
                full_text = "\n\n".join([f"[Page {p['page_number']}]\n{p['text']}" for p in pages])
                txt_file = txt_dir / f"{pdf_file.stem}.txt"
                txt_file.write_text(full_text, encoding="utf-8")
                print(f"Saved TXT: {txt_file.name}")


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    process_all_pdfs(save_txt=True)
    print("PDF ingestion complete!")
