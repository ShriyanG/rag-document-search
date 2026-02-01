from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
)
from config.llm_config import get_max_input_tokens, get_model_type
import torch
from .base import BaseLLM

class LocalLLM(BaseLLM):
    """
    Wrapper for local LLMs, supporting:
      - Causal (decoder-only) models like GPT
      - Seq2Seq (encoder-decoder) models like T5/Flan-T5

    Args:
        model_name (str): Hugging Face model identifier or local path
        model_type (str): 'causal' or 'seq2seq'
        device (str): 'cpu' or 'cuda'
        max_length (int): Maximum token length for generation
    """

    def __init__(
        self,
        model_name: str,
        model_type: str = None,
        device: str = "cpu",
        max_length: int = None,
    ):
        self.model_name = model_name
        self.device = device
        
        # Get from config if not provided
        if model_type is None:
            model_type = get_model_type(model_name)
        if max_length is None:
            max_length = get_max_input_tokens(model_name)
        
        self._model_type = model_type
        self.max_length = max_length

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if model_type == "causal":
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, device_map=None, low_cpu_mem_usage=True
            )
        elif model_type == "seq2seq":
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name, device_map=None, low_cpu_mem_usage=True
            )
        else:
            raise ValueError("model_type must be 'causal' or 'seq2seq'")

        self.model.to(self.device)
        self.model.eval()

    def get_max_tokens(self) -> int:
        """Return max tokens for this model."""
        return self.max_length

    def get_model_type(self) -> str:
        """Return model type."""
        return self._model_type

    def generate(self, prompt: str, max_length: int = None, **generation_kwargs) -> str:
        """
        Generate text from a prompt.

        Args:
            prompt: Input prompt
            max_length: Max tokens (uses model default if None)
            **generation_kwargs: Additional generation parameters

        Returns:
            Generated text as string
        """
        if max_length is None:
            max_length = self.max_length
            
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Merge default generation settings with any overrides
        default_kwargs = {"max_length": max_length, "do_sample": True}
        default_kwargs.update(generation_kwargs)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **default_kwargs)

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded

