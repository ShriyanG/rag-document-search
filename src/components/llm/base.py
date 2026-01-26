from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Abstract base class for all LLMs."""

    @abstractmethod
    def generate(self, prompt: str, max_length: int = None, **kwargs) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input prompt to generate from
            max_length: Maximum length of generated text
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text as string
        """
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """Return the maximum tokens this model can handle."""
        pass
    
    @abstractmethod
    def get_model_type(self) -> str:
        """Return the type of model (local, api, etc)."""
        pass
    @abstractmethod
    def get_model_type(self) -> str:
        """Return the model type (causal, seq2seq, openai)."""
        pass