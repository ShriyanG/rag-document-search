# src/rag_pipeline.py

from typing import List, Dict
from components.llm import LocalLLM, OpenAILLM
from retrieval import retrieve

# ----------------------------
# LLM Selection
# ----------------------------

# Choose your LLM implementation
llm = LocalLLM(
    model_name="google/flan-t5-small",
    model_type="seq2seq",
    device="cpu",
    max_length=256
)
# llm = OpenAILLM(model_name="gpt-4", api_key="YOUR_API_KEY")

# ----------------------------
# Helper Functions
# ----------------------------

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


# ----------------------------
# RAG Pipeline
# ----------------------------

def run_rag_pipeline(query: str, top_k: int = 5, max_tokens: int = 250) -> str:
    """
    End-to-end RAG pipeline:
    1. Retrieve top-k relevant chunks from vector store
    2. Format them for LLM consumption
    3. Generate answer from LLM
    """
    retrieved_chunks = retrieve(query=query, top_k=top_k)
    if not retrieved_chunks:
        return "No relevant documents found."
    context = format_context(retrieved_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    answer = llm.generate(prompt=prompt, max_length=max_tokens)
    return answer


# ----------------------------
# Entry Point for Testing
# ----------------------------

if __name__ == "__main__":
    test_query = "Explain the process of chunking and retrieval in the RAG pipeline."
    answer = run_rag_pipeline(test_query, top_k=10)
    
    print("-" * 80)
    print("Query:", test_query)
    print("Generated Answer:\n", answer)
