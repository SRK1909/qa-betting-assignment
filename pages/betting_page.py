from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BettingPage:
    def __init__(self, driver):
        self.driver = driver
        # Standard timeout for dynamic elements
        self.wait = WebDriverWait(driver, 15)
        
        # --- Locators identified via DOM Inspection ---
        # Unique ID for the Home odds button (Spec 2.1)
        self.HOME_ODDS_BUTTON = (By.ID, "odds-premier-league-manutd-chelsea-home")
        
        # Updated Stake input field ID from your latest screenshot (Spec 2.2)
        self.STAKE_INPUT = (By.ID, "bet-slip-stake-input")
        
        # Explicit ID for the Place Bet submission button (Spec 31)
        self.PLACE_BET_BUTTON = (By.ID, "bet-slip-place-bet")
        
        # Success receipt modal (Spec 2.4)
        self.SUCCESS_MODAL = (By.XPATH, "//*[contains(text(), 'Bet Placed Successfully')]")

    def select_home_win(self):
        """Clicks the '1' odds button for the first match[cite: 22]."""
        btn = self.wait.until(EC.element_to_be_clickable(self.HOME_ODDS_BUTTON))
        btn.click()

    def enter_stake(self, amount):
        """
        Enters the wager amount into the bet slip[cite: 29].
        Stake input accepts numeric values with up to 2 decimal places.
        """
        field = self.wait.until(EC.visibility_of_element_located(self.STAKE_INPUT))
        field.clear()
        # Sending keys as string to ensure precision and compatibility [cite: 81]
        field.send_keys(str(amount))

    def click_place_bet(self):
        """Submits the bet placement[cite: 31, 34]."""
        # Button resolves to success modal or error modal [cite: 36, 37]
        btn = self.wait.until(EC.element_to_be_clickable(self.PLACE_BET_BUTTON))
        btn.click()

    def verify_success_receipt(self):
        """Confirms the success receipt modal appears[cite: 40, 43]."""
        return self.wait.until(EC.presence_of_element_located(self.SUCCESS_MODAL)).is_displayed()