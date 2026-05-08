import pytest
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_api_place_bet_validation():
    """
    API Test: Verifies successful bet placement and business rule compliance.
    Rationale: Validates the backend contract, currency, and payout logic 
    directly to ensure financial integrity[cite: 187, 188].
    """
    # 1. Setup Environment and Data
    base_url = os.getenv("BASE_URL")
    user_id = os.getenv("USER_ID")
    
    with open('test_data.json') as f:
        data = json.load(f)
    stake_amount = data["ui_test_data"]["valid_stake"]

    # 2. Define Request Headers and Body [cite: 85, 106-109]
    headers = {
        "x-user-id": user_id,
        "Content-Type": "application/json"
    }
    
    payload = {
        "matchId": "premier-league-manutd-chelsea",
        "selection": "HOME",
        "stake": stake_amount
    }

    # 3. Execute POST Request [cite: 104, 105]
    response = requests.post(
    f"{base_url.rstrip('/')}/api/place-bet", 
    headers=headers, 
    json=payload
)

    # 4. Assertions (The "Contract Check")
    # Status Code must be 200 OK [cite: 111]
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    
    response_data = response.json()
    
    # Validate Currency [cite: 67, 119]
    # Note: We know BUG-003 exists where API returns USD instead of EUR
    assert response_data["currency"] == "EUR", f"Currency mismatch! Found: {response_data['currency']}"
    
    # Validate Payout Math [cite: 50, 213]
    expected_payout = round(payload["stake"] * response_data["odds"], 2)
    assert response_data["payout"] == expected_payout, f"Payout calculation error! Expected {expected_payout}"

    # Validate mandatory fields [cite: 112-118]
    assert "matchId" in response_data
    assert "stake" in response_data