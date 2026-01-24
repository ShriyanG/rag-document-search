from pathlib import Path
# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).parent.parent
PDF_DIR = BASE_DIR / "data/pdfs"
PROCESSED_DIR = BASE_DIR / "data/processed"

# Subfolders under processed
PICKLE_DIR = PROCESSED_DIR / "pickle"       # for pickled raw text
TEXT_DIR = PROCESSED_DIR / "text"           # for human-readable text
CHUNKS_DIR = PROCESSED_DIR / "chunks"       # for chunked data
EMBEDDINGS_DIR = PROCESSED_DIR / "embeddings"  # for embeddings

# ----------------------------
# Chunking Settings
# ----------------------------
CHUNK_SIZE = 500      # Maximum characters per chunk
CHUNK_OVERLAP = 50    # Number of overlapping characters between chunks

# ----------------------------
# Embedding Settings
# ----------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
