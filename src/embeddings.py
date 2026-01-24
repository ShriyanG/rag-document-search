import pickle
from pathlib import Path
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    CHUNKS_DIR,
    EMBEDDINGS_DIR,
    EMBEDDING_MODEL_NAME
)


def load_chunks() -> List[Dict]:
    """
    Load chunked text with metadata from disk.
    """
    chunks_path = CHUNKS_DIR / "chunks.pkl"
    with open(chunks_path, "rb") as f:
        return pickle.load(f)


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

    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            "embedding": embedding,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        })

    return embedded_chunks


def save_embeddings(embedded_chunks: List[Dict]) -> None:
    """
    Persist embeddings to disk.
    """
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EMBEDDINGS_DIR / "embeddings.pkl"

    with open(output_path, "wb") as f:
        pickle.dump(embedded_chunks, f)


def run_embedding_pipeline() -> None:
    """
    End-to-end embedding generation pipeline.
    """
    chunks = load_chunks()
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embedded_chunks = generate_embeddings(chunks, model)
    save_embeddings(embedded_chunks)


if __name__ == "__main__":
    run_embedding_pipeline()