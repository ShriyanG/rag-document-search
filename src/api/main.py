"""
FastAPI backend for RAG Document Search
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.pipeline import run_rag_pipeline, set_llm
from config.settings import DEFAULT_LLM_MODEL

app = FastAPI(
    title="RAG Document Search API",
    description="Query documents using Retrieval-Augmented Generation",
    version="0.1.0"
)


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
