from typing import Optional
from .base import BaseLLM

import openai

class OpenAILLM(BaseLLM):
    """OpenAI API wrapper."""

    def __init__(self, model_name: str = "gpt-4", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        # openai.api_key = api_key

    def generate(self, query: str, context: str, max_tokens: int = 500) -> str:
        """
        Implement the API call to OpenAI.
        Currently a placeholder.
        """
        # response = openai.Completion.create(
        #     engine=self.model_name,
        #     prompt=f"Context:\n{context}\n\nQuestion: {query}",
        #     max_tokens=max_tokens
        # )
        # return response.choices[0].text.strip()
        return "OpenAI API placeholder answer."
