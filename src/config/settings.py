# ----------------------------
# Chunking Settings
# ----------------------------
CHUNK_SIZE = 500      # Maximum characters per chunk
CHUNK_OVERLAP = 50    # Number of overlapping characters between chunks

# ----------------------------
# Embedding Settings
# ----------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# ----------------------------
# Retrieval Settings
# ----------------------------
DEFAULT_TOP_K = 5  # Default number of results to retrieve

# ----------------------------
# LLM Settings
# ----------------------------
DEFAULT_LLM_MODEL = "google/flan-t5-small"  # Default LLM model
DEFAULT_LLM_PROVIDER = "local"  # 'local' for Hugging Face, 'openai' for OpenAI
DEFAULT_LLM_DEVICE = "cpu"  # 'cpu' or 'cuda'

# Supported models
SUPPORTED_LOCAL_MODELS = [
    "google/flan-t5-small",
    "google/flan-t5-base",
    "google/flan-t5-large",
    "google/flan-t5-xl",
    "gpt2",
]

SUPPORTED_OPENAI_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
]

# ----------------------------
# Generation Settings
# ----------------------------
DEFAULT_MAX_TOKENS = 250  # Default max tokens for LLM generation
