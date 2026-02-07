"""
FastAPI backend for RAG Document Search
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.pipeline import run_rag_pipeline, set_llm
from config.settings import DEFAULT_LLM_MODEL
from config.paths import EMBEDDINGS_DIR, INDEX_PATH, CHUNKS_DIR, PDF_DIR

app = FastAPI(
    title="RAG Document Search API",
    description="Query documents using Retrieval-Augmented Generation",
    version="0.1.0"
)

# Track if setup has been run
_setup_complete = False


def check_and_run_setup():
    """Check if required files exist, run setup if needed"""
    global _setup_complete
    
    if _setup_complete:
        return True
    
    # Check if required files exist
    embeddings_file = EMBEDDINGS_DIR / "embeddings.pkl"
    chunks_file = CHUNKS_DIR / "chunks.pkl"
    index_file = INDEX_PATH / "index.faiss"
    
    if embeddings_file.exists() and chunks_file.exists() and index_file.exists():
        print("✅ All required files found. System ready.")
        _setup_complete = True
        return True
    
    print("⚠️ Required files missing. Running setup pipeline...")
    print(f"Checking: {embeddings_file} - {embeddings_file.exists()}")
    print(f"Checking: {chunks_file} - {chunks_file.exists()}")
    print(f"Checking: {index_file} - {index_file.exists()}")
    
    try:
        from components.data.pdf import PDFDataSource
        from retrieval.embeddings import run_embedding_pipeline
        from retrieval.indexing import run_vector_store_pipeline
        
        # Check if PDFs exist locally first
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        
        # If no local PDFs, try syncing from Supabase
        if not pdf_files:
            print("No local PDFs found. Attempting to sync from Supabase...")
            pdf_source = PDFDataSource()
            try:
                pdf_source.sync()
                pdf_files = list(PDF_DIR.glob("*.pdf"))
            except Exception as sync_error:
                print(f"Supabase sync failed: {sync_error}")
        
        if not pdf_files:
            print(f"❌ No PDF files found in {PDF_DIR} and Supabase sync failed")
            print("Please either:")
            print("  1. Add PDF files to data/pdfs/ directory, or")
            print("  2. Configure Supabase credentials in .env")
            return False
        
        print(f"Step 1: Processing {len(pdf_files)} PDF(s)...")
        pdf_source = PDFDataSource()
        pdf_source.process(save_txt=True)
        
        print("Step 2: Generating embeddings...")
        run_embedding_pipeline()
        
        print("Step 3: Building FAISS index...")
        run_vector_store_pipeline()
        
        print("✅ Setup complete!")
        _setup_complete = True
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


@app.on_event("startup")
async def startup_event():
    """Run setup check on startup"""
    print("🚀 Starting RAG Document Search API...")
    check_and_run_setup()


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    llm_model: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    top_k: int
    model: str


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "RAG Document Search API",
        "version": "0.1.0"
    }


@app.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    """
    Query the RAG pipeline with a question.
    
    Args:
        request: QueryRequest with query, top_k, and optional llm_model
        
    Returns:
        QueryResponse with the generated answer
    """
    try:
        # Set LLM if specified
        model_name = request.llm_model or DEFAULT_LLM_MODEL
        if request.llm_model:
            set_llm(request.llm_model)
        
        # Run RAG pipeline
        answer = run_rag_pipeline(
            query=request.query,
            top_k=request.top_k,
            llm_model=request.llm_model
        )
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            top_k=request.top_k,
            model=model_name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "rag-document-search",
        "default_model": DEFAULT_LLM_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
