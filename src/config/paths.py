from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).parent.parent.parent
PDF_DIR = BASE_DIR / "data/pdfs"
PROCESSED_DIR = BASE_DIR / "data/processed"
ENV_PATH = Path('.') / '.env'
TEST_PDF_DIR = BASE_DIR / "tests/test_data/pdfs"

# Subfolders under processed
PICKLE_DIR = PROCESSED_DIR / "pickle"       # for pickled raw text
TEXT_DIR = PROCESSED_DIR / "text"           # for human-readable text
CHUNKS_DIR = PROCESSED_DIR / "chunks"       # for chunked data
EMBEDDINGS_DIR = PROCESSED_DIR / "embeddings"  # for embeddings

# Vector store index
INDEX_PATH = PROCESSED_DIR / "vector_index.index"
