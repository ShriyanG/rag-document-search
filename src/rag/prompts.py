"""
Prompt templates and formatting utilities for the RAG pipeline.
"""


def create_prompt(query: str, context: str) -> str:
    """
    Create a prompt for the LLM using the query and retrieved context.

    Args:
        query: The user's question
        context: The formatted context from retrieved chunks

    Returns:
        A formatted prompt string
    """
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    return prompt


def create_qa_prompt(question: str, context: str, style: str = "default") -> str:
    """
    Create a QA-style prompt with optional style customization.

    Args:
        question: The question to answer
        context: The context from retrieved documents
        style: Prompt style ('default', 'detailed', 'concise')

    Returns:
        Formatted prompt string
    """
    if style == "detailed":
        return f"""Based on the following context, provide a detailed answer to the question.

Context:
{context}

Question: {question}

Detailed Answer:"""

    elif style == "concise":
        return f"""Answer the following question in one sentence using the context provided.

Context:
{context}

Question: {question}

Answer:"""

    else:  # default
        return f"""Context:
{context}

Question: {question}

Answer:"""
