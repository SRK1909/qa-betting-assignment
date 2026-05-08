# Part A: Manual QA & Test Strategy - Test Plan

**Target Application:** `https://qae-assignment-tau.vercel.app/`
**Test User ID:** `candidate-c8Lm5Tr9VX`

---

## Scenario TC-01: E2E Single Bet Placement (Degraded Happy Path)
* **Priority:** Critical
* **Risk Rationale:** This is the core revenue-generating flow. If users cannot successfully place a valid bet, see their balance accurately update dynamically, and receive the correct API contract data, the platform fails its primary commercial objective.
* **Steps:**
  1. Navigate to the application URL with the authenticated user ID. Note the starting balance.
  2. Locate the first available match, click the '1' (Home) odds button, and verify the bet slip opens.
  3. Enter a valid stake of `15.00`.
  4. Open DevTools (Network tab) and click 'Place Bet'.
* **Expected Result:** The stake is deducted. A success receipt modal appears displaying the correct Bet ID, Match details, Selection, Stake, Odds, Potential Payout, and Timestamp.
* **Crucial State & Contract Checks:** * The API response payload MUST return `"currency": "EUR"`.
  * The API response payload MUST return a unique server-generated `betId` and `timestamp`.
  * The UI Header balance MUST update dynamically to reflect the deducted balance without requiring a page refresh.

## Scenario TC-02: Minimum Stake Enforcement (Requirements Conflict)
* **Priority:** High
* **Risk Rationale:** Validating edge cases around financial rules prevents revenue leakage and API rejection loops. The specification explicitly states the minimum stake is €1.00.
* **Steps:**
  1. Authenticate via the user ID URL.
  2. Select an outcome for any match to populate the bet slip.
  3. Enter a stake of exactly `1.00`.
  4. Open DevTools (Network tab) and click 'Place Bet'.
* **Expected Result:** The system accepts the bet successfully and triggers the success receipt, verifying that the system correctly enforces the €1.00 minimum boundary. 

## Scenario TC-03: Maximum Stake Limit (Upper Boundary)
* **Priority:** High
* **Risk Rationale:** Enforcing maximum stake limits mitigates financial exposure and platform liability on single wagers.
* **Steps:**
  1. Authenticate via the user ID URL.
  2. Select an outcome for any match to populate the bet slip.
  3. Enter a stake of exactly `100.00`.
  4. Click 'Place Bet'.
* **Expected Result:** The bet is successfully placed if funds are sufficient.
* **Sub-test (Negative):** Enter a stake of `100.01`. The system prevents the bet placement and displays an error indicating the maximum stake limit has been exceeded.

## Scenario TC-04: Insufficient Funds Block (Validation Overlap)
* **Priority:** Critical
* **Risk Rationale:** Financial liability risk. The system must never expose the business to credit risk by allowing wagers that exceed the user's settled, available balance.
* **Precondition Check (Validation Overlap):** Ensure the user's balance is **below €100.00** before executing this test. If the balance is above €100 (e.g., €115), attempting an insufficient funds bet (e.g., €116) will trigger the "Maximum Stake" validation first, masking the true "Insufficient Funds" behavior.
* **Steps:**
  1. Authenticate via the user ID URL.
  2. If the balance is > €100, place a valid wager to reduce the balance below €100.00 (e.g., to €98.50).
  3. Select an outcome for a match.
  4. Enter a stake value exactly `€0.50` higher than the current available balance (e.g., `99.00`), ensuring it is still below the €100 max limit.
  5. Click 'Place Bet'.
* **Expected Result:** The placement is blocked. The UI explicitly displays an "Insufficient balance" message. The user's available balance remains unchanged.

## Scenario TC-05: Odds Override & State Reset (Functional)
* **Priority:** Medium
* **Risk Rationale:** UX friction and state corruption. Because the platform only supports single bets, the bet slip must cleanly overwrite the existing state rather than appending to it or crashing when a user changes their mind.
* **Steps:**
  1. Authenticate via the user ID URL.
  2. Click the '1' (Home) odds button for Match A.
  3. Verify the bet slip shows 'HOME' for Match A.
  4. Click the '2' (Away) odds button for the same Match A.
  5. Click the 'X' (Draw) odds button for a completely different Match B.
* **Expected Result:** Selecting new odds replaces the previous selection entirely. The bet slip should only ever show one active selection at a time, ultimately ending with Match B - Draw. Financial stake must reset to 0.00 upon override to prevent accidental wagers.

## Scenario TC-06: Decimal Precision Constraint (Data Sanitization)
* **Priority:** Medium
* **Risk Rationale:** Floating-point arithmetic errors can cause payout miscalculations. The system must strictly enforce standard EUR currency precision formatting.
* **Steps:**
  1. Authenticate via the user ID URL.
  2. Select an outcome for a match.
  3. Enter a stake of `10.555` (3 decimal places).
  4. Attempt to place the bet.
* **Expected Result:** The UI input field should automatically restrict the input to a maximum of 2 decimal places, truncating or preventing the third digit. If the UI allows it, the API must return a semantic validation failure.