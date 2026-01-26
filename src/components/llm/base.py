from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Abstract base class for all LLMs."""

    @abstractmethod
    def generate(self, query: str, context: str, max_tokens: int = 200) -> str:
        """Generate a response given a query and context."""
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """Return the maximum tokens this model can handle."""
        pass
    
    @abstractmethod
    def get_model_type(self) -> str:
        """Return the model type (causal, seq2seq, openai)."""
        pass