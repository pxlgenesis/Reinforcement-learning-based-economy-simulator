# Pre-Retraining Improvements & Learnings Report
**Date:** November 25, 2025
**Status:** Ready for 2nd Training Run

## 1. The Initial Problem (Why the 1st Model Failed)
Our first training run revealed critical flaws in the simulation's economic physics, leading to unrealistic outcomes that the AI could not solve.

*   **The "Instant Monopoly" Bug**: A single firm could hire 100% of the workforce in a single month by offering $0.01 more than competitors.
*   **The "Winner-Takes-All" Goods Market**: Consumers always bought from the absolute cheapest firm, causing that firm to sell out instantly while others starved, leading to a single dominant mega-corp.
*   **The "Stagflation Trap"**: Firms would raise prices infinitely while production collapsed, leading to high inflation and 100% unemployment.
*   **Infinite Growth**: There were no limits on how big a firm could get, allowing a "Garage Startup" to become Amazon in 3 months without any infrastructure investment.

## 2. Diagnosis & Key Learnings
Through diagnostic runs and code analysis, we learned:

1.  **Friction is Essential**: Real economies have friction. People don't switch jobs every month for a 1% raise. Without friction (contracts), the labor market is too volatile for stable learning.
2.  **Scale has Limits**: In the real world, adding the 100th employee is less efficient than the 1st. In our sim, it was linear, which encouraged infinite hoarding of labor.
3.  **Infrastructure Costs Money**: You cannot run a 500-person company with $0 overhead. We needed a mechanism to force firms to "pay to grow."
4.  **Inflation Breaks Static Rules**: Fixed costs (like "$20,000 startup capital") become meaningless when inflation hits 1000%. All costs must be dynamic/relative to the price level.

## 3. Implemented Solutions (The "Stability Patch")

We implemented a comprehensive set of "Physics Patches" to fix these issues before retraining the AI.

### A. Labor Market Reforms
*   **Employment Contracts**: Workers are now locked into **6-month contracts**. They cannot quit or be poached unless the new offer is significantly higher (1.5x). This stabilizes the workforce.
*   **Hiring Friction**: Firms can only hire if they have the cash reserves to pay wages for 3 months.

### B. Production & Growth Limits
*   **Diminishing Returns**: Implemented a power law (`Production = Skill ^ 0.9`). This makes massive firms less efficient per worker, naturally encouraging a multi-firm ecosystem.
*   **Firm Tiers (The "Hard Cap")**:
    *   **Tier 1 (Startup)**: Max 5 Employees.
    *   **Tier 2 (Small Biz)**: Max 20 Employees. (Upgrade Cost: High)
    *   **Tier 3 (Medium)**: Max 50 Employees.
    *   **Tier 4 (Corp)**: Max 200 Employees.
    *   **Result**: Firms must accumulate significant capital and "level up" to grow. They cannot just hire everyone instantly.

### C. Goods Market Logic
*   **Limited Search**: Consumers now check **3 random firms** instead of the entire market. This gives smaller/slightly more expensive firms a chance to make sales, preventing the "Winner-Takes-All" collapse.

### D. Inflation-Proofing
*   **Dampened Upgrade Costs**: We learned that if upgrade costs scale linearly with inflation, they become impossible to afford during high inflation. We implemented a `sqrt(price_ratio)` scaling to allow firms to "catch up" and upgrade even in inflationary periods.
*   **Dynamic Bailouts**: Bankrupt firms now receive restart capital proportional to the current wage level, not a fixed $20k.

## 4. Diagnostic Results
After implementing these changes, we ran a 200-step diagnostic simulation.
*   **Stability**: The economy no longer collapses into a single monopoly.
*   **Churn**: Firms rise, upgrade, fail, and restart in a healthy cycle.
*   **Market Share**: The largest firm typically holds 10-15% of the market, spiking to 40% only when it successfully upgrades to a higher tier (which is the intended reward for investment).
*   **Conclusion**: The environment is now robust enough for the AI to learn meaningful fiscal policies.

## 5. Next Steps
*   **Retrain PPO Agent**: With these stability rules, the agent should now be able to learn the delicate balance of Tax vs. Spending without breaking the game physics.
*   **New Observation Space**: We added `Real GDP`, `Govt Cash`, and `Subsistence Failures` to the agent's inputs so it can see the consequences of its actions.
