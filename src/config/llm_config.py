# LLM Model configurations with token limits
LLM_CONFIGS = {
    "google/flan-t5-small": {
        "type": "seq2seq",
        "max_input_tokens": 512,
        "max_output_tokens": 256,
    },
    "google/flan-t5-base": {
        "type": "seq2seq",
        "max_input_tokens": 512,
        "max_output_tokens": 256,
    },
    "google/flan-t5-large": {
        "type": "seq2seq",
        "max_input_tokens": 512,
        "max_output_tokens": 256,
    },
    "gpt2": {
        "type": "causal",
        "max_input_tokens": 1024,
        "max_output_tokens": 256,
    },
    "meta-llama/Llama-2-7b": {
        "type": "causal",
        "max_input_tokens": 4096,
        "max_output_tokens": 512,
    },
    "gpt-4": {
        "type": "openai",
        "max_input_tokens": 8192,
        "max_output_tokens": 2048,
    },
}

def get_llm_config(model_name: str) -> dict:
    """Get configuration for a model."""
    if model_name in LLM_CONFIGS:
        return LLM_CONFIGS[model_name]
    # Default for unknown models
    return {
        "type": "causal",
        "max_input_tokens": 512,
        "max_output_tokens": 256,
    }

def get_max_output_tokens(model_name: str) -> int:
    """Get max output tokens for a model."""
    return get_llm_config(model_name)["max_output_tokens"]

def get_max_input_tokens(model_name: str) -> int:
    """Get max input tokens for a model."""
    return get_llm_config(model_name)["max_input_tokens"]

def get_model_type(model_name: str) -> str:
    """Get the type of model."""
    return get_llm_config(model_name)["type"]