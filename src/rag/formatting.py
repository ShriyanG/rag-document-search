from typing import List, Dict


def format_context(chunks: List[Dict]) -> str:
    """
    Prepare retrieved chunks for the LLM.
    - Concatenate text from multiple chunks
    - Include metadata like filename/page
    """
    context_parts = []
    for chunk in chunks:
        meta = chunk["metadata"]
        context_parts.append(
            f"[{meta['filename']} - Page {meta['page_number']}] {chunk['text']}"
        )
    return "\n\n".join(context_parts)
