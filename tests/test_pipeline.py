# Test RAG pipeline
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag import run_rag_pipeline, format_context
from rag.prompts import create_prompt


def test_format_context():
    """Test context formatting."""
    try:
        chunks = [
            {
                "text": "Sample text 1",
                "metadata": {"filename": "test.pdf", "page_number": 1}
            },
            {
                "text": "Sample text 2",
                "metadata": {"filename": "test.pdf", "page_number": 2}
            }
        ]
        context = format_context(chunks)
        assert "Sample text 1" in context
        assert "Sample text 2" in context
        print("✓ test_format_context passed")
    except Exception as e:
        print(f"✗ test_format_context failed: {e}")


def test_create_prompt():
    """Test prompt creation."""
    try:
        prompt = create_prompt("What is AI?", "Context about AI")
        assert "What is AI?" in prompt
        assert "Context about AI" in prompt
        print("✓ test_create_prompt passed")
    except Exception as e:
        print(f"✗ test_create_prompt failed: {e}")


if __name__ == "__main__":
    test_format_context()
    test_create_prompt()
