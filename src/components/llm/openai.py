from typing import Optional
import os
from .base import BaseLLM

try:
    import openai
except ImportError:
    openai = None

class OpenAILLM(BaseLLM):
    """
    OpenAI API wrapper for GPT models.
    
    Args:
        model_name: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
        api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
        max_tokens: Maximum tokens for generation
    """

    def __init__(
        self, 
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        max_tokens: int = 2048
    ):
        if openai is None:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.model_name = model_name
        self.max_tokens = max_tokens
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Set API key for openai package
        openai.api_key = self.api_key

    def generate(self, prompt: str, max_length: int = None, **kwargs) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Input prompt
            max_length: Max tokens (uses model default if None)
            **kwargs: Additional parameters for API (temperature, top_p, etc)
            
        Returns:
            Generated text as string
        """
        if max_length is None:
            max_length = self.max_tokens
        
        try:
            # Use the new openai client interface (v1.0+)
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length,
                **kwargs
            )
            
            return response.choices[0].message.content.strip()
        
        except AttributeError:
            # Fall back to legacy openai interface (v0.x)
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length,
                **kwargs
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def get_max_tokens(self) -> int:
        """Return max tokens for this model."""
        return self.max_tokens

    def get_model_type(self) -> str:
        """Return model type."""
        return "openai_api"

