import re
from typing import List, Dict


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


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters between chunks
    
    Returns:
        List of text chunks
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
