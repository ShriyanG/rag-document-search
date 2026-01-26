from typing import List, Dict

from retrieval import retrieve
from components.llm import LocalLLM
from config.llm_config import get_max_output_tokens, get_model_type, get_max_input_tokens
from .formatting import format_context
from .prompts import create_prompt


# ----------------------------
# LLM Selection
# ----------------------------

MODEL_NAME = "google/flan-t5-small"
MAX_OUTPUT_TOKENS = get_max_output_tokens(MODEL_NAME)
MAX_INPUT_TOKENS = get_max_input_tokens(MODEL_NAME)  # Add this

llm = LocalLLM(
    model_name=MODEL_NAME,
    model_type=get_model_type(MODEL_NAME),
    device="cpu",
    max_length=MAX_OUTPUT_TOKENS
)


# ----------------------------
# Token Management Utilities
# ----------------------------

def estimate_tokens(text: str) -> int:
    """
    Rough estimate of token count (1 token ≈ 4 characters).
    For accurate count, use tokenizer from llm.tokenizer.
    """
    return len(text) // 4


def calculate_optimal_top_k(query: str, max_attempts: int = 10) -> int:
    """
    Dynamically calculate the optimal top_k that fits within token limit.
    
    Args:
        query: The user's question
        max_attempts: Maximum documents to try (starts high, reduces if needed)
    
    Returns:
        Optimal top_k value that won't exceed token limit
    """
    # Reserve tokens for query + prompt structure + output
    reserved_tokens = estimate_tokens(query) + 100  
    available_for_context = MAX_INPUT_TOKENS - reserved_tokens
    
    # Try progressively smaller top_k values
    for top_k in range(max_attempts, 0, -1):
        retrieved_chunks = retrieve(query=query, top_k=top_k)
        
        if not retrieved_chunks:
            continue
        
        context = format_context(retrieved_chunks)
        context_tokens = estimate_tokens(context)
        
        # Check if this top_k fits
        total_tokens = reserved_tokens + context_tokens
        
        if total_tokens <= MAX_INPUT_TOKENS:
            print(f"📊 Optimal top_k: {top_k} (total tokens: {total_tokens}/{MAX_INPUT_TOKENS})")
            return top_k
    
    # If nothing fits, return 1
    return 1


# ----------------------------
# RAG Pipeline
# ----------------------------

def run_rag_pipeline(query: str, top_k: int = None, max_tokens: int = None) -> str:
    """
    End-to-end RAG pipeline with dynamic token optimization.

    Args:
        query: The question
        top_k: Number of documents to retrieve (None = auto-calculate)
        max_tokens: Max output tokens (None = use model default)
    """
    # Use model's default if not specified
    if max_tokens is None:
        max_tokens = MAX_OUTPUT_TOKENS
    
    # Dynamically calculate top_k
    top_k = calculate_optimal_top_k(query)
    
    retrieved_chunks = retrieve(query=query, top_k=top_k)
    if not retrieved_chunks:
        return "No relevant documents found."
    
    context = format_context(retrieved_chunks)
    prompt = create_prompt(query, context)
    answer = llm.generate(prompt=prompt, max_length=max_tokens)
    return answer


# ----------------------------
# Entry Point for Testing
# ----------------------------

if __name__ == "__main__":
    test_query = "Explain the process of chunking and retrieval in the RAG pipeline."
    answer = run_rag_pipeline(test_query)  # top_k auto-calculated!

    print("-" * 80)
    print("Query:", test_query)
    print("Generated Answer:\n", answer)
