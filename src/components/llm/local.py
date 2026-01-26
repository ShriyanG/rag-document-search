from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
)
import torch
class LocalLLM:
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
        model_type: str = "causal",
        device: str = "cpu",
        max_length: int = 512,
    ):
        self.model_name = model_name
        self.model_type = model_type
        self.device = device
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

    def generate(self, prompt: str, **generation_kwargs) -> str:
        """
        Generate text from a prompt.

        Returns the decoded string output.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Merge default generation settings with any overrides
        default_kwargs = {"max_length": self.max_length, "do_sample": True}
        default_kwargs.update(generation_kwargs)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **default_kwargs)

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded
