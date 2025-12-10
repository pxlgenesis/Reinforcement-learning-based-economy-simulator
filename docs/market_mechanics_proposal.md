# Market Mechanics Overhaul Proposal: Solving the "Winner Takes All"

## 1. The Problem
Currently, the simulation exhibits a "Monopoly Mode" where one firm captures all employees. This happens because:
1.  **Frictionless Labor Market**: Workers instantly switch to the highest bidder every month.
2.  **Linear Scalability**: A firm with 100 workers is exactly 10x more productive than a firm with 10. There is no downside to infinite growth.
3.  **No Capacity Limits**: A startup with $20k can theoretically hire 100 people if it had the cash flow, without any infrastructure limits.

## 2. Proposed Solutions

### A. Labor Market Friction (Loyalty & Contracts)
**Goal**: Prevent the entire workforce from moving to a single firm in one step.

1.  **Employment Contracts**:
    *   When hired, a worker signs a contract for `X` months (e.g., 6 months).
    *   During this period, they **cannot** quit for a higher wage unless the wage difference is extreme (>50% increase).
    *   *Effect*: Slows down the rate at which a monopoly can drain talent from competitors.

2.  **Churn Probability**:
    *   Even without better offers, there is a natural turnover rate (e.g., 2% per month).
    *   Only these "churning" workers + the unemployed enter the job market each month.
    *   *Effect*: Stabilizes firm sizes.

### B. Firm Evolution & Tiers
**Goal**: Create a progression system where firms must "level up" to handle more workers.

| Tier | Name | Max Employees | Inventory Cap | Fixed Cost (Overhead) | Upgrade Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Startup** | 5 | 1,000 | $500/mo | - |
| 2 | **Small Biz** | 20 | 5,000 | $2,000/mo | $50,000 |
| 3 | **Medium Ent** | 50 | 20,000 | $10,000/mo | $200,000 |
| 4 | **Corporation** | 200 | 100,000 | $50,000/mo | $1,000,000 |

*   **Implementation**:
    *   Firms start at Tier 1.
    *   They cannot hire beyond `Max Employees`.
    *   They must save cash to pay the `Upgrade Cost` to reach the next tier.
    *   *Effect*: Prevents a lucky startup from instantly becoming a monopoly. They have to grow organically.

### C. Diminishing Returns (The Natural Cap)
**Goal**: Make it inefficient to be too big without scaling infrastructure.

*   **Current Formula**: `Production = Productivity * Total_Skill` (Linear)
*   **New Formula**: `Production = Productivity * (Total_Skill ^ 0.9)`
*   *Effect*: The 100th worker adds less value than the 1st worker due to bureaucracy/inefficiency. Eventually, the cost of the worker > value added, naturally stopping growth.

### D. Skill-Based Hiring
**Goal**: Differentiate firms by quality.

*   **Logic**:
    *   **Tier 1/2 Firms**: Can only utilize `Skill <= 1.5`. High skill workers are wasted here (capped productivity).
    *   **Tier 3/4 Firms**: Can utilize full skill.
    *   *Result*: High skill workers will naturally prefer larger firms (if they pay for the skill), while low skill workers populate startups.

## 3. Implementation Plan (Phased)

**Phase 1: The "Sticky" Update (Recommended First Step)**
*   Implement **Contracts** (6-month lock).
*   Implement **Diminishing Returns** (Power law production).
*   *Why?* This requires minimal code changes but immediately stops the "instant monopoly" behavior.

**Phase 2: The "Tiers" Update**
*   Add `Firm.level`, `Firm.max_employees`.
*   Add logic for upgrading.
*   *Why?* Adds depth and strategy for the RL agent (needs to foster an environment where firms *can* upgrade).

## 4. Discussion
Do you agree with starting with **Phase 1**? It directly addresses the "random firm captures everyone" issue by making employees "sticky" and making massive scale less efficient.
