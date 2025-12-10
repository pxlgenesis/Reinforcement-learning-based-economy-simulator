# Pre-Implementation Review: Market Mechanics Overhaul

## 1. Assessment of Proposed Changes
The proposed changes (Contracts, Tiers, Diminishing Returns) are **highly recommended** to solve the "Winner Takes All" instability. They introduce necessary friction and capacity constraints that mirror real-world economics.

## 2. Logic & Compatibility Check

### A. The "Startup Trap" (Critical Risk)
*   **Issue**: If Tier 1 is capped at 5 employees and has fixed overhead, it might be mathematically impossible to save enough for Tier 2.
*   **Scenario**:
    *   Max Revenue (Tier 1) = 5 workers * Productivity * Price.
    *   Max Profit = Revenue - Wages - **Fixed Overhead**.
    *   If Fixed Overhead is static ($500) and inflation is low, this might be a huge burden.
    *   If inflation is high, $500 is nothing.
*   **Fix**: Fixed Overhead must be **dynamic**, scaling with `Avg Price` (e.g., `50 * Avg_Price`).

### B. Contract Logic vs Bankruptcy
*   **Issue**: When a firm goes bankrupt (`_restructure`), it fires everyone.
*   **Check**: Does the `Household` know its contract is void?
*   **Current Code**: `Household` checks `if employer_id not in firms: is_employed = False`.
*   **Refinement**: We must ensure that when `Firm` clears `self.employees`, the `AgentManager` updates the `Household` state to `contract_remaining = 0`.

### C. Diminishing Returns vs AI Learning
*   **Issue**: The RL Agent (Government) might get confused if GDP drops initially because large firms become less efficient.
*   **Mitigation**: This is acceptable. The agent needs to learn that "More Small Firms > One Giant Firm".

## 3. Refined Implementation Plan

### Step 1: Household Contracts (The "Sticky" Fix)
*   Modify `Household`: Add `contract_remaining` (int).
*   Modify `AgentManager`:
    *   In Labor Market, only unemployed OR `contract_remaining == 0` look for jobs.
    *   Exception: If `new_wage > current_wage * 1.5`, break contract (poaching).
    *   Decrement `contract_remaining` every step.

### Step 2: Diminishing Returns (The "Efficiency" Fix)
*   Modify `Firm`:
    *   Update `produce_goods`: `production = productivity * (total_skill ** 0.9)`.
    *   This naturally penalizes massive scaling without upgrades (future).

### Step 3: Firm Tiers (The "Growth" Fix) - *Deferred to Phase 2*
*   We will implement Tiers *after* stabilizing with Steps 1 & 2.
*   We need to balance the math for Upgrade Costs carefully.

## 4. Conclusion
The logic holds up, provided we handle the **Bankruptcy -> Contract Void** edge case and ensure **Overhead scales with Inflation**.

**Recommendation**: Proceed with Step 1 (Contracts) and Step 2 (Diminishing Returns) immediately.
