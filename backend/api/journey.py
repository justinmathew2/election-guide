from fastapi import APIRouter, Response
from pydantic import BaseModel
from core.journey import global_journey, JourneyState
from core.zkp import generate_eligibility_proof

router = APIRouter()

class JourneyResponse(BaseModel):
    """Response model for journey state."""
    state: JourneyState

class EligibilityRequest(BaseModel):
    """Request model for verifying eligibility."""
    age: int
    location: str

class EligibilityResponse(BaseModel):
    """Response model containing eligibility result and optional ZKP proof."""
    is_eligible: bool
    zkp_proof: str | None
    message: str

@router.get("/state", response_model=JourneyResponse)
def get_journey_state(response: Response) -> JourneyResponse:
    """
    Returns the current state of the voter journey.
    """
    # Allow caching for 5 seconds to reduce redundant hits while remaining reasonably fresh
    response.headers["Cache-Control"] = "public, max-age=5"
    return JourneyResponse(state=global_journey.get_state())

@router.post("/advance", response_model=JourneyResponse)
def advance_journey() -> JourneyResponse:
    """
    Advances the voter journey to the next logical state.
    """
    return JourneyResponse(state=global_journey.advance())

@router.post("/reset", response_model=JourneyResponse)
def reset_journey() -> JourneyResponse:
    """
    Resets the voter journey back to the initial state.
    """
    return JourneyResponse(state=global_journey.reset())

@router.post("/verify-eligibility", response_model=EligibilityResponse)
def verify_eligibility(req: EligibilityRequest) -> EligibilityResponse:
    """
    Verifies user eligibility and generates a Zero-Knowledge Proof (simulated).
    """
    result = generate_eligibility_proof(req.age, req.location)
    return EligibilityResponse(**result)
