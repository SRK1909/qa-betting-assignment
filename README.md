## 1. Framework Architecture
The framework is built using Python 3.13, leveraging industry-standard libraries for cross-layer validation:

UI Layer: Selenium WebDriver using the Page Object Model (POM) to ensure locator stability and code reusability.

API Layer: Python Requests library for rapid business rule validation and backend contract testing.

Configuration: python-dotenv for secure environment management and JSON for externalized test data.

## 2. Prerequisites
Before running the tests, ensure you have the following:

Python 3.8+ (Developed on 3.13)

Google Chrome (The framework uses webdriver-manager to automate driver setup)

Pip (Python package manager)

---

## 3. Installation & Setup
### 3.1 Clone the Repository
   ```powershell
   git clone https://github.com/SRK1909/qa-betting-assignment.git
   cd qa-betting-assignment
    ```
---
### 3.2 Install Dependencies
   ```powershell
    pip install -r requirements.txt
    ```
---
### 3.3 Configure Environment Variables
    Create a `.env` file in the root directory and add your credentials:
    ```
    BASE_URL=https://qae-assignment-tau.vercel.app/
    USER_ID=your-unique-candidate-id-here
    ```
---

## 4. Running the Automation
The framework uses Pytest for execution. You can run the entire suite or isolate specific layers.

### 4.1 Run Full Suite (UI + API)
```powershell
python -m pytest tests/ -v -s
```

### 4.2 Run UI E2E Test Only
```powershell
python -m pytest tests/test_ui_e2e.py -v -s
```

### 4.3 Run API Test Only
```powershell
python -m pytest tests/test_api.py -v -s
```

## 5. Interpreting Results
UI Test: Validates the successful placement of a bet and the appearance of the success receipt modal per the feature specification.

API Test (Expected Failure): This test is specifically designed to catch BUG-003 (Currency Mismatch). It will fail with an AssertionError because the API returns USD instead of the required EUR. This failure confirms the automation is correctly identifying backend contract violations.

## 6. Directory Structure
qa-betting-assignment/
├── assets/                 # Manual testing evidence (screenshots)
├── pages/                  # Page Object Model locators and actions
│   ├── __init__.py
│   └── betting_page.py
├── tests/                  # UI and API test scripts
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_ui_e2e.py
├── .env                    # Environment variables (URL, User ID)
├── .gitignore              # Prevents tracking of pycache and secrets
├── requirements.txt        # Python library dependencies
├── test_data.json          # Externalized test parameters (Stake values)
├── test_plan.md            # Part A: Strategic Manual Test Plan
├── execution_and_bugs.md   # Part A: Bug Reports and Results
└── strategy_and_recommendations.md # Part C: Strategy & Scaling


