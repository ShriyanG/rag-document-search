from typing import List, Dict, Optional

from retrieval import retrieve
from components.llm import LLMFactory
from config.settings import DEFAULT_LLM_MODEL, DEFAULT_MAX_TOKENS
from config.llm_config import get_max_output_tokens, get_max_input_tokens
from .formatting import format_context
from .prompts import create_prompt


# ----------------------------
# Global LLM Instance
# ----------------------------

# This will be set by set_llm() or default to configured model
_llm = None


def set_llm(model_name: str = DEFAULT_LLM_MODEL, **kwargs):
    """
    Set the global LLM instance.
    
    Args:
        model_name: Name of the LLM model
        **kwargs: Additional arguments for LLM creation (api_key, device, etc)
    """
    global _llm
    print(f"Loading LLM: {model_name}...")
    _llm = LLMFactory.create(model_name, **kwargs)
    print(f"✓ LLM loaded: {model_name}")


def get_llm():
    """Get the current LLM instance, initializing with default if needed."""
    global _llm
    if _llm is None:
        set_llm(DEFAULT_LLM_MODEL)
    return _llm


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
    llm = get_llm()
    max_input_tokens = get_max_input_tokens(llm.model_name)
    
    # Reserve tokens for query + prompt structure + output
    reserved_tokens = estimate_tokens(query) + 100  
    available_for_context = max_input_tokens - reserved_tokens
    
    # Try progressively smaller top_k values
    for top_k in range(max_attempts, 0, -1):
        retrieved_chunks = retrieve(query=query, top_k=top_k)
        
        if not retrieved_chunks:
            continue
        
        context = format_context(retrieved_chunks)
        context_tokens = estimate_tokens(context)
        
        # Check if this top_k fits
        total_tokens = reserved_tokens + context_tokens
        
        if total_tokens <= max_input_tokens:
            print(f"📊 Optimal top_k: {top_k} (total tokens: {total_tokens}/{max_input_tokens})")
            return top_k
    
    # If nothing fits, return 1
    return 1


# ----------------------------
# RAG Pipeline
# ----------------------------

def run_rag_pipeline(
    query: str,
    top_k: int = None,
    max_tokens: int = None,
    llm_model: Optional[str] = None
) -> str:
    """
    End-to-end RAG pipeline with dynamic token optimization and LLM switching.

    Args:
        query: The question
        top_k: Number of documents to retrieve (None = auto-calculate)
        max_tokens: Max output tokens (None = use model default)
        llm_model: Optional LLM model to use (switches LLM if provided)
        
    Returns:
        Generated answer as string
    """
    # Switch LLM if specified
    if llm_model is not None:
        set_llm(llm_model)
    
    llm = get_llm()
    
    # Use model's default if not specified
    if max_tokens is None:
        max_tokens = get_max_output_tokens(llm.model_name)
    
    # Dynamically calculate top_k if not specified
    if top_k is None:
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
    answer = run_rag_pipeline(test_query)  # Uses default LLM with auto-calculated top_k

    print("-" * 80)
    print("Query:", test_query)
    print("Generated Answer:\n", answer)

