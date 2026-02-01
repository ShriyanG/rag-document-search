"""
Storage factory for creating and switching between storage backends.

Dynamically loads supported backends. Storage backend is configured
via config/settings.py and environment variables.
"""

from typing import Optional
from .base import BaseStorage
from .local import LocalStorage
from .supabase import SupabaseStorage


class StorageFactory:
    """
    Factory for creating storage instances.
    
    Supports:
    - Local filesystem storage (testing/development)
    - Supabase bucket storage (production)
    
    Easily extensible for other cloud providers.
    """

    # Supported storage backends
    SUPPORTED_BACKENDS = {
        "local": LocalStorage,
        "supabase": SupabaseStorage,
    }

    @staticmethod
    def create(
        backend: str = "local",
        **kwargs
    ) -> BaseStorage:
        """
        Create a storage instance.
        
        Args:
            backend: Storage backend name ('local' or 'supabase')
            **kwargs: Backend-specific arguments:
                - local: base_dir (Path)
                - supabase: bucket_name (str), supabase_url (str), supabase_key (str)
            
        Returns:
            BaseStorage instance
            
        Raises:
            ValueError: If backend not supported or required kwargs missing
        """
        if backend not in StorageFactory.SUPPORTED_BACKENDS:
            supported = list(StorageFactory.SUPPORTED_BACKENDS.keys())
            raise ValueError(
                f"Unknown storage backend: {backend}. "
                f"Supported backends: {supported}"
            )
        
        backend_class = StorageFactory.SUPPORTED_BACKENDS[backend]
        
        try:
            return backend_class(**kwargs)
        except TypeError as e:
            raise ValueError(
                f"Missing required arguments for {backend} storage: {e}"
            )

    @staticmethod
    def list_backends() -> dict:
        """
        List all supported storage backends.
        
        Returns:
            Dict mapping backend names to their classes
        """
        return StorageFactory.SUPPORTED_BACKENDS.copy()

    @staticmethod
    def register_backend(name: str, backend_class: type) -> None:
        """
        Register a new storage backend.
        
        Args:
            name: Name of the backend (e.g., 'aws-s3')
            backend_class: Class that inherits from BaseStorage
            
        Raises:
            ValueError: If backend_class doesn't inherit from BaseStorage
        """
        if not issubclass(backend_class, BaseStorage):
            raise ValueError(
                f"{backend_class.__name__} must inherit from BaseStorage"
            )
        StorageFactory.SUPPORTED_BACKENDS[name] = backend_class


# Convenience function for easy import
def create_storage(
    backend: str = "local",
    **kwargs
) -> BaseStorage:
    """
    Convenience function to create a storage instance.
    
    Args:
        backend: Storage backend name ('local' or 'supabase')
        **kwargs: Backend-specific arguments
        
    Returns:
        BaseStorage instance
    """
    return StorageFactory.create(backend, **kwargs)
