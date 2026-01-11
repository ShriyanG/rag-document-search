from pathlib import Path
# Paths
BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "data/pdfs"
PROCESSED_DIR = BASE_DIR / "data/processed"

# Chunking Settings
CHUNK_SIZE = 500      # Maximum characters per chunk
CHUNK_OVERLAP = 50    # Number of overlapping characters between chunks