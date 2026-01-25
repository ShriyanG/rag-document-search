# Test LLM components
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from components.llm import BaseLLM, LocalLLM, OpenAILLM


def test_local_llm_instantiation():
    """Test that LocalLLM can be instantiated."""
    try:
        llm = LocalLLM(
            model_name="google/flan-t5-small",
            model_type="seq2seq",
            device="cpu",
            max_length=256
        )
        assert llm is not None
        print("✓ test_local_llm_instantiation passed")
    except Exception as e:
        print(f"✗ test_local_llm_instantiation failed: {e}")


def test_base_llm_abstract():
    """Test that BaseLLM is abstract."""
    try:
        BaseLLM()  # Should fail - cannot instantiate abstract class
        print("✗ test_base_llm_abstract failed: BaseLLM should be abstract")
    except TypeError:
        print("✓ test_base_llm_abstract passed")


if __name__ == "__main__":
    test_local_llm_instantiation()
    test_base_llm_abstract()
