from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import advisor, journey

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
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Election Guide API", "docs": "/docs"}

# Include routers
app.include_router(advisor.router, prefix="/api/advisor", tags=["Advisor"])
app.include_router(journey.router, prefix="/api/journey", tags=["Journey"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
