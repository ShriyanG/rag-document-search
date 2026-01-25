from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from config import CHUNKS_DIR, EMBEDDINGS_DIR, EMBEDDING_MODEL_NAME
from utils import load_pickle, save_pickle


def load_chunks() -> List[Dict]:
    """Load chunked text with metadata from disk."""
    return load_pickle(CHUNKS_DIR, "chunks.pkl")


def generate_embeddings(
    chunks: List[Dict],
    model: SentenceTransformer
) -> List[Dict]:
    """
    Generate embeddings for each chunk.
    """
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return [
        {
            "embedding": embedding,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]


def save_embeddings(embedded_chunks: List[Dict]) -> None:
    """Persist embeddings to disk."""
    save_pickle(EMBEDDINGS_DIR, embedded_chunks, "embeddings.pkl")


def run_embedding_pipeline() -> None:
    """End-to-end embedding generation pipeline."""
    chunks = load_chunks()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embedded_chunks = generate_embeddings(chunks, model)
    save_embeddings(embedded_chunks)


if __name__ == "__main__":
    run_embedding_pipeline()