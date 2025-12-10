# Simulation Anomaly Report: The "Hyper-Growth" Event

## 1. The Anomaly
**Observation**:
*   **Scenario**: User set Income Tax = 100%, Corporate Tax = 100%, UBI = 1000.
*   **Expectation**: Economic collapse (Starvation, 0 GDP).
*   **Reality**: Exponential GDP growth ($53M+), Hyperinflation ($13k Prices), 50% Unemployment.

## 2. Root Cause Analysis
The simulation is currently operating as a **Fiat Currency System with Unlimited Deficit Spending**.

### A. The "Magic Money" Printer (UBI)
*   **Code**: `h.cash += ubi` (AgentManager).
*   **Issue**: UBI is injected directly into household wallets without being deducted from a Government Budget.
*   **Impact**: Even with 100% taxes, the government is effectively "printing" $100,000 per month (100 households * $1000). This ensures demand never drops to zero.

### B. The Inflationary Bailout Loop
*   **Code**: `bailout_cash = max(Initial, wage_offer * 60)` (Firm).
*   **Issue**: Bailouts are calculated based on *current wage offers*.
*   **Impact**: As inflation rises, wages rise. As wages rise, bailouts become larger.
    *   If a firm fails with wages at $100, it gets $6,000.
    *   If a firm fails with wages at $10,000, it gets $600,000.
    *   This injects exponentially more money into the system, fueling further inflation.

### C. The Wage-Price Spiral
*   **Mechanism**:
    1.  Households spend UBI -> Demand remains high.
    2.  Firms raise prices to match demand (`price * 1.05`).
    3.  Firms raise wages to hire workers (`wage * 1.10` Panic Hiring).
    4.  Higher wages -> Higher Bailouts -> More Money -> Higher Prices.

## 3. Why Taxes Didn't Stop It
*   Taxes remove money *after* it has circulated.
*   With 100% tax, the "Velocity of Money" is effectively 1 (Government -> Household -> Firm -> Government).
*   However, the **Volume** of money is constantly increasing due to the Bailout Loop and fixed UBI injection.

## 4. Recommendations for "Realistic" Mode
To fix this and make the economy behave like a real constrained system:

1.  **Implement Government Budget Constraint**:
    *   Govt starts with $0.
    *   UBI can only be paid if `Govt Cash > 0`.
    *   If `Govt Cash < 0`, UBI stops (Austerity).

2.  **Deflationary Bailouts**:
    *   Bailouts should be fixed or capped, not proportional to runaway wages.
    *   Or, bailouts should come from Tax Revenue (Bailout Fund), not printed money.

3.  **Central Bank Logic**:
    *   If Inflation > 5%, the system should trigger a "Recession" (reduce money supply) rather than printing more.

## 5. Conclusion
The current behavior is **mathematically correct** for the rules defined (Modern Monetary Theory on steroids), but **economically unrealistic** for a stable simulation. The AI exploited the "Printing Press" to maximize GDP (Nominal) despite 100% taxes.
