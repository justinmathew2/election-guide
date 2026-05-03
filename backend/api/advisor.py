import os
import time
import hashlib
import logging
import vertexai
from vertexai.preview import rag
from vertexai.generative_models import GenerativeModel, Tool
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.cloud.logging

from core.secrets import get_secret

router = APIRouter()

# Set up local fallback logger
fallback_logger = logging.getLogger(__name__)

# Initialize Google Cloud Logging
try:
    logging_client = google.cloud.logging.Client()
    logger = logging_client.logger("election-advisor-analytics")
except Exception as e:
    fallback_logger.warning(f"Cloud Logging init failed (fallback to console): {e}")
    logger = fallback_logger

# Attempt to load Project ID from Secret Manager (fallback to env)
PROJECT_ID = get_secret("VERTEX_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)

class QuestionRequest(BaseModel):
    """Request model for asking the advisor a question."""
    question: str

class AnswerResponse(BaseModel):
    """Response model for the advisor's answer."""
    answer: str

# Global cache for corpus name and model to improve efficiency
_CACHED_CORPUS_NAME = None
_CACHED_MODEL = None

def get_corpus_name() -> str:
    """
    Retrieves the RAG corpus name, caching it after the first successful read.
    """
    global _CACHED_CORPUS_NAME
    if _CACHED_CORPUS_NAME:
        return _CACHED_CORPUS_NAME
        
    try:
        corpus_file_path = os.path.join(os.path.dirname(__file__), "..", "core", "corpus_name.txt")
        if os.path.exists(corpus_file_path):
            with open(corpus_file_path, "r") as f:
                _CACHED_CORPUS_NAME = f.read().strip()
                return _CACHED_CORPUS_NAME
    except OSError as e:
        if logger:
            logger.error(f"OS error reading corpus file: {e}")
    except Exception as e:
        if logger:
            logger.error(f"Unexpected error reading corpus file: {e}")
        
    # Fallback to environment variable
    _CACHED_CORPUS_NAME = os.getenv("RAG_CORPUS_NAME", "")
    return _CACHED_CORPUS_NAME

def get_model():
    """
    Returns a cached instance of the GenerativeModel configured with the RAG tool.
    """
    global _CACHED_MODEL
    if _CACHED_MODEL:
        return _CACHED_MODEL
        
    corpus_name = get_corpus_name()
    if not corpus_name:
        return None
        
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=[corpus_name],
                similarity_top_k=5,
            ),
        )
    )
    
    _CACHED_MODEL = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        tools=[rag_retrieval_tool],
        system_instruction=(
            "You are an expert Election Advisor. Your role is to guide users on election rules, "
            "timelines, and registration steps. Answer questions based ONLY on the provided election documents. "
            "If the information is not in the documents, state that you do not know."
        )
    )
    return _CACHED_MODEL

@router.post("/ask", response_model=AnswerResponse)
async def ask_advisor(request: QuestionRequest) -> AnswerResponse:
    """
    Handles user questions by querying the Vertex AI RAG corpus with optimized caching.
    """
    model = get_model()
    if not model:
        raise HTTPException(
            status_code=500, 
            detail="RAG Corpus Name not configured. Please run backend/core/ingest.py first."
        )
        
    start_time = time.time()
    
    # Generate the response
    response = model.generate_content(request.question)
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Log anonymized query (SHA-256 hash) and latency
    if logger:
        anonymized_query_hash = hashlib.sha256(request.question.encode("utf-8")).hexdigest()
        log_payload = {
            "query_hash": anonymized_query_hash,
            "latency_ms": latency_ms,
            "status": "success",
        }
        if hasattr(logger, "log_struct"):
            logger.log_struct(log_payload, severity="INFO")
        else:
            logger.info(f"Analytics: {log_payload}")
    
    return AnswerResponse(answer=response.text)
