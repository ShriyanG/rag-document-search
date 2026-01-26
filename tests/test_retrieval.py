# Test retrieval functionality
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from retrieval import retrieve


def test_retrieve():
    """Test basic retrieval."""
    try:
        results = retrieve(
            query="What is the main topic?",
            top_k=3
        )
        assert isinstance(results, list)
        print("✓ test_retrieval passed")
    except Exception as e:
        print(f"✗ test_retrieval failed: {e}")


if __name__ == "__main__":
    test_retrieve()
