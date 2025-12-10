# Model Training Parameters & Features (Proposed)

## 1. Overview
To solve the "Stagflation Trap" (High Inflation + High Unemployment) and the "Infinite Money Glitch" (Unconstrained Spending), we are redefining the environment parameters for the next training run.

## 2. Observation Space (Inputs)
The agent needs to see the full picture, including its own bank account.

| Index | Feature | Description | New/Existing |
| :--- | :--- | :--- | :--- |
| 0 | **Unemployment Rate** | % of workforce without jobs (0.0 - 1.0) | Existing |
| 1 | **Avg Price** | Current average price of goods | Existing |
| 2 | **Avg Wage** | Current average wage | Existing |
| 3 | **Tax Revenue** | Total tax collected in last step | Existing |
| 4 | **Real GDP** | Nominal GDP adjusted for inflation (Base Price = 10.0) | **NEW** (Replaces Nominal GDP) |
| 5 | **Gini Coefficient** | Inequality measure (0.0 = Perfect Equality, 1.0 = Perfect Inequality) | Existing |
| 6 | **Subsistence Failures** | Count of households that starved (Game Over metric) | Existing |
| 7 | **Govt Cash** | The government's current treasury balance | **NEW** |

## 3. Action Space (Outputs)
The agent controls fiscal policy.

| Index | Action | Range | Description |
| :--- | :--- | :--- | :--- |
| 0 | **Income Tax** | 0% - 80% | Tax on household income |
| 1 | **Corporate Tax** | 0% - 80% | Tax on firm profits |
| 2 | **UBI (Subsidy)** | 0 - 200 Credits | Monthly payment to every household |

## 4. Reward Function (The Goal)
We must align the agent's incentives with a healthy economy.

**Formula:**
$$ R = (RealGDP_{growth} \times 2.0) - (Unemployment \times 5.0) - (Inflation_{penalty}) - (Deficit_{penalty}) $$

### Components:
1.  **Real GDP Growth**:
    *   Reward the agent for increasing *production*, not just prices.
    *   Use `log(Real GDP)` to encourage steady growth rather than exponential spikes.
2.  **Unemployment Penalty**:
    *   Heavy penalty if unemployment > 10%.
    *   `if unemployment > 0.10: penalty = (unemployment - 0.10) * 20.0`
3.  **Inflation Penalty**:
    *   Punish rapid price changes (both hyperinflation and deflation).
    *   `penalty = abs(current_price - last_price) / last_price`
4.  **Deficit Penalty (Soft Constraint)**:
    *   The agent is allowed to spend, but if `Govt Cash < 0` (or near 0), it gets penalized.
    *   Actually, the environment now *hard constrains* spending (UBI checks bounce if no cash), so the penalty is the resulting poverty/death (Subsistence Failures).
    *   We can add a small penalty for `Govt Cash < 1000` to encourage building a safety net.

## 5. Training Configuration
*   **Algorithm**: PPO (Proximal Policy Optimization)
*   **Timesteps**: 500,000 (approx 2 hours)
*   **Entropy Coefficient**: 0.01 (Encourage exploration early on)
*   **Learning Rate**: 3e-4 (Standard)

## 6. Expected Outcome
*   **No Hyperinflation**: Real GDP reward punishes price hikes without production.
*   **Sustainable Budget**: Hard constraints + poverty penalties force the agent to tax before spending.
*   **Low Unemployment**: The agent learns that employed workers = tax payers = higher budget = higher score.
