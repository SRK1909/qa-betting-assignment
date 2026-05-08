import os
import json
import pytest
from pages.betting_page import BettingPage

def test_tc01_e2e_single_bet_placement(driver):
    """
    E2E UI Test: Verifies the critical user journey.
    Rationale: Uses externalized test data for better maintainability.
    """
    # 1. Load Test Data from external JSON
    with open('test_data.json') as f:
        data = json.load(f)
    
    input_stake = data["ui_test_data"]["valid_stake"]
    
    # 2. Setup Auth
    base_url = os.getenv("BASE_URL")
    user_id = os.getenv("USER_ID")
    driver.get(f"{base_url.rstrip('/')}/?user-id={user_id}")
    
    # 3. Execute Steps
    betting_page = BettingPage(driver)
    betting_page.select_home_win()
    betting_page.enter_stake(input_stake) 
    betting_page.click_place_bet()
    
    # 4. Verify Outcome
    assert betting_page.verify_success_receipt()