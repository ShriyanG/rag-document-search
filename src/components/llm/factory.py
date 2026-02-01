"""
LLM Factory for creating and switching between different LLM implementations.

Models are loaded dynamically from config/settings.py, so updates there
automatically reflect in the factory without code changes.
"""

from typing import Optional, Dict, Any
from .base import BaseLLM
from .local import LocalLLM
from .openai import OpenAILLM
from config.settings import SUPPORTED_LOCAL_MODELS, SUPPORTED_OPENAI_MODELS


class LLMFactory:
    """
    Factory class for creating LLM instances.
    
    Supports:
    - Local Hugging Face models (e.g., 'flan-t5-small')
    - OpenAI API models (e.g., 'gpt-4', 'gpt-3.5-turbo')
    
    Models are dynamically loaded from config/settings.py
    """

    # Supported LLM providers
    SUPPORTED_PROVIDERS = {
        "local": LocalLLM,
        "openai": OpenAILLM,
    }

    @staticmethod
    def _build_model_to_provider_mapping() -> Dict[str, str]:
        """
        Build model to provider mapping from config.
        
        Returns:
            Dict mapping model names to provider names
        """
        mapping = {}
        
        # Add local models from config
        for model in SUPPORTED_LOCAL_MODELS:
            mapping[model] = "local"
        
        # Add OpenAI models from config
        for model in SUPPORTED_OPENAI_MODELS:
            mapping[model] = "openai"
        
        return mapping

    @property
    @staticmethod
    def MODEL_TO_PROVIDER() -> Dict[str, str]:
        """
        Get model to provider mapping (built from config).
        
        This is dynamic - updates to config/settings.py are automatically
        reflected without restarting the application.
        """
        return LLMFactory._build_model_to_provider_mapping()

    @staticmethod
    def create(
        model_name: str,
        provider: Optional[str] = None,
        **kwargs
    ) -> BaseLLM:
        """
        Create an LLM instance.
        
        Args:
            model_name: Name of the model (e.g., 'gpt-4', 'flan-t5-small')
            provider: Explicit provider ('local' or 'openai'). 
                     If None, auto-detects from model name
            **kwargs: Additional arguments to pass to the LLM constructor
            
        Returns:
            BaseLLM instance
            
        Raises:
            ValueError: If provider not supported or model not found
        """
        
        # Get dynamic model mapping from config
        model_mapping = LLMFactory._build_model_to_provider_mapping()
        
        # Auto-detect provider if not specified
        if provider is None:
            provider = model_mapping.get(model_name)
            if provider is None:
                raise ValueError(
                    f"Unknown model: {model_name}. "
                    f"Supported models: {list(model_mapping.keys())}"
                )
        
        # Validate provider
        if provider not in LLMFactory.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Supported providers: {list(LLMFactory.SUPPORTED_PROVIDERS.keys())}"
            )
        
        # Get the LLM class
        llm_class = LLMFactory.SUPPORTED_PROVIDERS[provider]
        
        # Create instance with model_name and any additional kwargs
        return llm_class(model_name=model_name, **kwargs)

    @staticmethod
    def list_models() -> Dict[str, list]:
        """
        List all supported models by provider.
        
        Dynamically loaded from config/settings.py, so reflects
        current configuration without restart.
        
        Returns:
            Dict mapping provider names to lists of model names
        """
        models_by_provider = {}
        model_mapping = LLMFactory._build_model_to_provider_mapping()
        
        for model, provider in model_mapping.items():
            if provider not in models_by_provider:
                models_by_provider[provider] = []
            models_by_provider[provider].append(model)
        
        return models_by_provider

    @staticmethod
    def register_model(model_name: str, provider: str) -> None:
        """
        Register a new model by adding it to config/settings.py
        
        Args:
            model_name: Name of the model
            provider: Provider ('local' or 'openai')
            
        Note:
            This is a convenience method. For permanent registration,
            add the model to SUPPORTED_LOCAL_MODELS or SUPPORTED_OPENAI_MODELS
            in config/settings.py
        """
        if provider not in LLMFactory.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        
        if provider == "local":
            if model_name not in SUPPORTED_LOCAL_MODELS:
                SUPPORTED_LOCAL_MODELS.append(model_name)
        elif provider == "openai":
            if model_name not in SUPPORTED_OPENAI_MODELS:
                SUPPORTED_OPENAI_MODELS.append(model_name)


# Convenience function for easy import
def create_llm(
    model_name: str,
    provider: Optional[str] = None,
    **kwargs
) -> BaseLLM:
    """Convenience function to create an LLM instance."""
    return LLMFactory.create(model_name, provider, **kwargs)
