from pathlib import Path
# Folder containing raw PDFs and processed text files
PDF_DIR = Path(__file__).parent.parent / "data" / "pdfs"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

# Ensure processed folder exists
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)