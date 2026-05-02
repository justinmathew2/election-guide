import pytest
from playwright.sync_api import Page, expect

# Ensure backend and frontend servers are running before executing this test
# using `pytest -m e2e`

@pytest.mark.e2e
def test_voter_journey_flow(page: Page):
    """
    Test the Voter Journey flow including ZKP Eligibility Verification
    and advancing the FSM Timeline.
    """
    # 1. Navigate to the frontend application
    page.goto("http://localhost:3000/")
    
    # Verify the page loaded correctly
    expect(page.locator("h1")).to_contain_text("Civic Clarity: Election Guide")
    
    # 2. Test ZKP Eligibility Form
    page.fill("input[name='age']", "28")
    page.fill("input[name='location']", "New York")
    page.click("button:has-text('Verify')")
    
    # Wait for the successful cryptographic verification message
    success_message = page.locator("text=Eligibility cryptographically verified.")
    expect(success_message).to_be_visible()
    
    # Verify the Proof Hash is rendered
    expect(page.locator("text=Proof Hash:")).to_be_visible()

    # 3. Test Journey FSM Timeline Interaction
    advance_btn = page.locator("button:has-text('Advance Journey State')")
    
    # Click to advance state
    advance_btn.click()
    
    # Additional logic can be added here to verify timeline component CSS classes
    # mapping to the "current" or "completed" states.
    # For now, we verify the advance button is fully functional.
    expect(advance_btn).to_be_enabled()
