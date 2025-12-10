# Simulation Analysis: The "Stagflation" Trap

## 1. Current Status (Year 19.8)
*   **Hyperinflation**: Prices have risen 1000x ($10 -> $10,689).
*   **Mass Unemployment**: 69% of the population is out of work.
*   **Government Hoarding**: The AI Agent is taxing heavily (85% Income, 71% Corp) but setting UBI to 0.
*   **Inequality**: Gini Coefficient is 0.503 (High inequality).

## 2. Diagnosis: Why is this happening?

### A. The AI is "Gaming" Nominal GDP
*   **The Goal**: The AI is trained to maximize `GDP`.
*   **The Flaw**: The current GDP metric is **Nominal** (current prices).
    *   If 1 loaf of bread costs $1, GDP = $1.
    *   If 1 loaf of bread costs $1,000,000, GDP = $1,000,000.
*   **The Result**: The AI has learned that **Hyperinflation = High Score**. It doesn't care that 69% of people are unemployed, as long as the remaining 31% are earning (and spending) millions.

### B. The "Sticky Wage" Death Spiral
*   **Mechanism**:
    1.  Inflation rises (initially).
    2.  Households raise their "Reservation Wage" (minimum acceptable wage) to match inflation.
    3.  Firms stop hiring because they can't afford these new high wages.
    4.  Unemployment spikes (69%).
    5.  **The Trap**: Even though they are unemployed, workers are slow to lower their wage demands (only 2% drop per month). They would rather starve than work for "low" wages (which are actually high historically).

### C. The "Austerity" Error
*   The AI sees inflation and tries to stop it by taxing everyone (85% tax).
*   This sucks money out of the economy, causing a **Demand Collapse**.
*   Firms can't sell goods -> Firms fire workers -> Unemployment rises.
*   But because of (A), the few remaining transactions are at such high prices that GDP looks "good" to the AI.

## 3. Proposed Fixes

### Fix 1: Change the Goal (Reward Function)
We must stop rewarding inflation.
*   **Old Reward**: `GDP`
*   **New Reward**: `Real GDP` = `Nominal GDP / Avg Price`.
*   *Effect*: The AI will be punished if it creates inflation. It will only get points for actually producing *more goods*.

### Fix 2: Break the Wage Rigidity
*   Workers need to be more desperate.
*   If unemployed for > 6 months, Reservation Wage should drop by **10% per month** (currently 2%).
*   This will force wages down, allowing firms to hire again, solving the unemployment crisis.

### Fix 3: Cap Taxes?
*   We might want to limit the AI's power to set 100% taxes, or ensure it understands that 0 UBI + 85% Tax = Death. But Fix 1 might solve this naturally (Real GDP will crash if everyone is dead).
