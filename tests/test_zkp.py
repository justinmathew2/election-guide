import pytest
from backend.core.zkp import generate_eligibility_proof

def test_eligible_voter_zkp():
    """Test ZKP logic for an eligible voter (age >= 18)."""
    result = generate_eligibility_proof(age=25, location="NY")
    
    assert result["is_eligible"] is True
    assert result["zkp_proof"] is not None
    # SHA-256 hash length is 64 characters
    assert len(result["zkp_proof"]) == 64
    assert result["message"] == "Eligibility cryptographically verified."

def test_ineligible_voter_zkp():
    """Test ZKP logic for an ineligible voter (age < 18)."""
    result = generate_eligibility_proof(age=16, location="CA")
    
    assert result["is_eligible"] is False
    assert result["zkp_proof"] is None
    assert result["message"] == "Ineligible."

def test_zkp_unique_salts():
    """Ensure two requests with same data get different proofs due to time/salt."""
    result1 = generate_eligibility_proof(age=30, location="TX")
    result2 = generate_eligibility_proof(age=30, location="TX")
    
    assert result1["zkp_proof"] != result2["zkp_proof"]

def test_zkp_invalid_inputs():
    """Test ZKP with edge cases like negative age or missing location."""
    # Negative age
    result = generate_eligibility_proof(age=-1, location="Mars")
    assert result["is_eligible"] is False
    
    # Empty location
    result = generate_eligibility_proof(age=20, location="")
    assert result["is_eligible"] is True  # Logic currently only checks age
    assert result["zkp_proof"] is not None

