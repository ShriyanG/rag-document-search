from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Abstract base class for all LLMs."""

    @abstractmethod
    def generate(self, query: str, context: str, max_tokens: int = 200) -> str:
        """
        Generate a response given a query and context.
        """
        pass