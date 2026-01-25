#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

print("Testing imports...\n")

try:
    from config import PDF_DIR, EMBEDDINGS_DIR, CHUNK_SIZE, EMBEDDING_MODEL_NAME
    print("✓ config imports")
except Exception as e:
    print(f"✗ config imports: {e}")

try:
    from utils import load_pickle, save_pickle, chunk_text, clean_text
    print("✓ utils imports")
except Exception as e:
    print(f"✗ utils imports: {e}")

try:
    from retrieval import retrieve, search_index, embed_query
    print("✓ retrieval imports")
except Exception as e:
    print(f"✗ retrieval imports: {e}")

try:
    from rag import run_rag_pipeline, format_context, create_prompt
    print("✓ rag imports")
except Exception as e:
    print(f"✗ rag imports: {e}")

try:
    from components import BaseLLM, LocalLLM, OpenAILLM
    print("✓ components.llm imports")
except Exception as e:
    print(f"✗ components.llm imports: {e}")

try:
    from components import BaseVectorStore, FAISSVectorStore
    print("✓ components.vectorstore imports")
except Exception as e:
    print(f"✗ components.vectorstore imports: {e}")

try:
    from components import BaseDataSource, PDFDataSource
    print("✓ components.data imports")
except Exception as e:
    print(f"✗ components.data imports: {e}")

print("\n✓ All imports successful!")
