import hashlib
import os
import time

SECRET_SALT = os.getenv("ZKP_SECRET_SALT", "election_super_secret_salt")

def generate_eligibility_proof(age: int, location: str) -> dict:
    """
    Simulates a Zero-Knowledge Proof (ZKP) by verifying eligibility (age >= 18)
    and generating a cryptographic commitment (hash) without returning
    or storing the raw data.
    """
    is_eligible = age >= 18
    
    # Create a simulated "proof" using a salted hash
    raw_data = f"{age}:{location}:{SECRET_SALT}:{time.time()}".encode('utf-8')
    proof_hash = hashlib.sha256(raw_data).hexdigest()
    
    return {
        "is_eligible": is_eligible,
        "zkp_proof": proof_hash if is_eligible else None,
        "message": "Eligibility cryptographically verified." if is_eligible else "Ineligible."
    }
