from fastapi import APIRouter
from pydantic import BaseModel
from core.journey import global_journey, JourneyState
from core.zkp import generate_eligibility_proof

router = APIRouter()

class JourneyResponse(BaseModel):
    state: JourneyState

class EligibilityRequest(BaseModel):
    age: int
    location: str

class EligibilityResponse(BaseModel):
    is_eligible: bool
    zkp_proof: str | None
    message: str

@router.get("/state", response_model=JourneyResponse)
def get_journey_state():
    return JourneyResponse(state=global_journey.get_state())

@router.post("/advance", response_model=JourneyResponse)
def advance_journey():
    return JourneyResponse(state=global_journey.advance())

@router.post("/reset", response_model=JourneyResponse)
def reset_journey():
    return JourneyResponse(state=global_journey.reset())

@router.post("/verify-eligibility", response_model=EligibilityResponse)
def verify_eligibility(req: EligibilityRequest):
    result = generate_eligibility_proof(req.age, req.location)
    return EligibilityResponse(**result)
