import logging
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from api import advisor, journey

# Configure standard logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Election Guide API",
    description="Backend API for the Election Guide Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://election-guide-app.web.app",
        "https://election-guide-app.firebaseapp.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Middleware to add standard security headers to every response.
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/")
def read_root() -> Dict[str, str]:
    """
    Root endpoint for general information and docs link.
    """
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Election Guide API", "docs": "/docs"}

# Include routers
app.include_router(advisor.router, prefix="/api/advisor", tags=["Advisor"])
app.include_router(journey.router, prefix="/api/journey", tags=["Journey"])

@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint for determining service status.
    """
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}


