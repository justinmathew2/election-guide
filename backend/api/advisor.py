import os
import time
import hashlib
import vertexai
from vertexai.preview import rag
from vertexai.generative_models import GenerativeModel, Tool
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.cloud.logging

from core.secrets import get_secret

router = APIRouter()

# Initialize Google Cloud Logging
try:
    logging_client = google.cloud.logging.Client()
    logger = logging_client.logger("election-advisor-analytics")
except Exception as e:
    print(f"Cloud Logging init failed (fallback to console): {e}")
    logger = None

# Attempt to load Project ID from Secret Manager (fallback to env)
PROJECT_ID = get_secret("VERTEX_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

def get_corpus_name():
    try:
        corpus_file_path = os.path.join(os.path.dirname(__file__), "..", "core", "corpus_name.txt")
        with open(corpus_file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.getenv("RAG_CORPUS_NAME", "")

@router.post("/ask", response_model=AnswerResponse)
async def ask_advisor(request: QuestionRequest):
    corpus_name = get_corpus_name()
    if not corpus_name:
        raise HTTPException(
            status_code=500, 
            detail="RAG Corpus Name not configured. Please run backend/core/ingest.py first."
        )
        
    start_time = time.time()
        
    # Define the RAG tool pointing to our election documents corpus
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=[corpus_name],
                similarity_top_k=5,
            ),
        )
    )
    
    # Initialize Gemini 1.5 Flash model with the RAG tool
    model = GenerativeModel(
        model_name="gemini-1.5-flash-001",
        tools=[rag_retrieval_tool],
        system_instruction=(
            "You are an expert Election Advisor. Your role is to guide users on election rules, "
            "timelines, and registration steps. Answer questions based ONLY on the provided election documents. "
            "If the information is not in the documents, state that you do not know."
        )
    )
    
    # Generate the response
    response = model.generate_content(request.question)
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    # Log anonymized query (SHA-256 hash) and latency
    if logger:
        anonymized_query_hash = hashlib.sha256(request.question.encode("utf-8")).hexdigest()
        logger.log_struct(
            {
                "query_hash": anonymized_query_hash,
                "latency_ms": latency_ms,
                "status": "success",
            },
            severity="INFO"
        )
    
    return AnswerResponse(answer=response.text)
