# Stability Rules & Logic Cross-Check

This document tracks the specific mathematical rules implemented in the code to ensure economic stability and prevent "stupid" crashes (e.g., negative cash, death spirals).

## 1. Household Logic (`household.py`)
*   **Subsistence Consumption**:
    *   *Rule*: Must consume 1 unit of inventory per step.
    *   *Code*: `_consume()` checks `inventory >= 1.0`.
    *   *Failure Mode*: If `inventory < 1`, `subsistence_failed = True`.
    *   *Safety*: Does NOT die/delete agent. Just flags failure for Reward penalty.
*   **Reservation Wage**:
    *   *Rule*: Will not work for less than `WAGE_FLOOR` (`SUBSISTENCE_COST`).
    *   *Rule (COLA)*: Reservation wage increases with Inflation Rate.
    *   *Code*: `if inflation > 0: reservation_wage *= (1 + inflation)`.
    *   *Safety*: Prevents "Real Wage Collapse" where prices skyrocket but wages stay flat, leading to demand collapse.
*   **Budgeting**:
    *   *Rule*: Spend 50% of surplus cash.
    *   *Code*: `budget = min(h.cash, 100 + (surplus * 0.5))` in `AgentManager`.
    *   *Safety*: `min(h.cash)` ensures they never spend more than they have.

## 2. Firm Logic (`firm.py`)
*   **Sticky Prices**:
    *   *Rule*: Max price change $\pm 5\%$ per step.
    *   *Code*: `np.clip(change, -0.05*price, 0.05*price)`.
    *   *Safety*: Prevents chaotic hyperinflation or deflation spikes.
*   **Hiring Budget**:
    *   *Rule*: Cannot hire unless cash > 3 months of wages.
    *   *Code*: `can_afford_hire = cash > wage * 3`.
    *   *Safety*: Prevents firms from hiring workers they can't pay (Fraud).
*   **Bankruptcy**:
    *   *Rule*: If `cash < 0`, reset.
    *   *Code*: `_restructure()` resets cash to `INITIAL/2` and fires everyone.
    *   *Safety*: Prevents "Zombie Firms" with negative billions in debt. Keeps the simulation running.

## 3. Market Logic (`agent_manager.py`)
*   **Tax Collection (TDS)**:
    *   *Rule*: Income tax deducted *before* wage payment.
    *   *Code*: `net_wage = wage - tax`.
    *   *Safety*: Prevents households from spending tax money on goods and going into debt to the government.
*   **Fair Shopping**:
    *   *Rule*: Randomize shopper order.
    *   *Code*: `random.shuffle(shoppers)`.
    *   *Safety*: Prevents Household #0 from hoarding all cheap goods every month.
*   **Panic Hiring**:
    *   *Rule*: If a firm fails to hire due to low wages, it raises wages aggressively (10%).
    *   *Code*: `if failed_to_hire: wage_offer *= 1.10`.
    *   *Safety*: Ensures wages catch up to inflation/reservation wages, preventing 100% unemployment traps.
# Stability Rules & Logic Cross-Check

This document tracks the specific mathematical rules implemented in the code to ensure economic stability and prevent "stupid" crashes (e.g., negative cash, death spirals).

## 1. Household Logic (`household.py`)
*   **Subsistence Consumption**:
    *   *Rule*: Must consume 1 unit of inventory per step.
    *   *Code*: `_consume()` checks `inventory >= 1.0`.
    *   *Failure Mode*: If `inventory < 1`, `subsistence_failed = True`.
    *   *Safety*: Does NOT die/delete agent. Just flags failure for Reward penalty.
*   **Reservation Wage**:
    *   *Rule*: Will not work for less than `WAGE_FLOOR` (`SUBSISTENCE_COST`).
    *   *Rule (COLA)*: Reservation wage increases with Inflation Rate.
    *   *Code*: `if inflation > 0: reservation_wage *= (1 + inflation)`.
    *   *Safety*: Prevents "Real Wage Collapse" where prices skyrocket but wages stay flat, leading to demand collapse.
*   **Budgeting**:
    *   *Rule*: Spend 50% of surplus cash.
    *   *Code*: `budget = min(h.cash, 100 + (surplus * 0.5))` in `AgentManager`.
    *   *Safety*: `min(h.cash)` ensures they never spend more than they have.

## 2. Firm Logic (`firm.py`)
*   **Sticky Prices**:
    *   *Rule*: Max price change $\pm 5\%$ per step.
    *   *Code*: `np.clip(change, -0.05*price, 0.05*price)`.
    *   *Safety*: Prevents chaotic hyperinflation or deflation spikes.
*   **Hiring Budget**:
    *   *Rule*: Cannot hire unless cash > 3 months of wages.
    *   *Code*: `can_afford_hire = cash > wage * 3`.
    *   *Safety*: Prevents firms from hiring workers they can't pay (Fraud).
*   **Bankruptcy**:
    *   *Rule*: If `cash < 0`, reset.
    *   *Code*: `_restructure()` resets cash to `INITIAL/2` and fires everyone.
    *   *Safety*: Prevents "Zombie Firms" with negative billions in debt. Keeps the simulation running.

## 3. Market Logic (`agent_manager.py`)
*   **Tax Collection (TDS)**:
    *   *Rule*: Income tax deducted *before* wage payment.
    *   *Code*: `net_wage = wage - tax`.
    *   *Safety*: Prevents households from spending tax money on goods and going into debt to the government.
*   **Fair Shopping**:
    *   *Rule*: Randomize shopper order.
    *   *Code*: `random.shuffle(shoppers)`.
    *   *Safety*: Prevents Household #0 from hoarding all cheap goods every month.
*   **Panic Hiring**:
    *   *Rule*: If a firm fails to hire due to low wages, it raises wages aggressively (10%).
    *   *Code*: `if failed_to_hire: wage_offer *= 1.10`.
    *   *Safety*: Ensures wages catch up to inflation/reservation wages, preventing 100% unemployment traps.
*   **Budget Commitment**:
    *   *Rule*: Firms cannot hire more workers than their *remaining* cash allows.
    *   *Code*: `committed_budget` tracker in `AgentManager`.
    *   *Safety*: Prevents firms from spending 100% of cash on wages and going bankrupt immediately.
*   **Inventory Rot**:
    *   *Rule*: 10% of unsold goods disappear.
    *   **Risk**: Floating Point Errors (e.g., Cash = -0.0000001).
# Stability Rules & Logic Cross-Check

This document tracks the specific mathematical rules implemented in the code to ensure economic stability and prevent "stupid" crashes (e.g., negative cash, death spirals).

## 1. Household Logic (`household.py`)
*   **Subsistence Consumption**:
    *   *Rule*: Must consume 1 unit of inventory per step.
    *   *Code*: `_consume()` checks `inventory >= 1.0`.
    *   *Failure Mode*: If `inventory < 1`, `subsistence_failed = True`.
    *   *Safety*: Does NOT die/delete agent. Just flags failure for Reward penalty.
*   **Reservation Wage**:
    *   *Rule*: Will not work for less than `WAGE_FLOOR` (`SUBSISTENCE_COST`).
    *   *Rule (COLA)*: Reservation wage increases with Inflation Rate.
    *   *Code*: `if inflation > 0: reservation_wage *= (1 + inflation)`.
    *   *Safety*: Prevents "Real Wage Collapse" where prices skyrocket but wages stay flat, leading to demand collapse.
*   **Budgeting**:
    *   *Rule*: Spend 50% of surplus cash.
    *   *Code*: `budget = min(h.cash, 100 + (surplus * 0.5))` in `AgentManager`.
    *   *Safety*: `min(h.cash)` ensures they never spend more than they have.

## 2. Firm Logic (`firm.py`)
*   **Sticky Prices**:
    *   *Rule*: Max price change $\pm 5\%$ per step.
    *   *Code*: `np.clip(change, -0.05*price, 0.05*price)`.
    *   *Safety*: Prevents chaotic hyperinflation or deflation spikes.
*   **Hiring Budget**:
    *   *Rule*: Cannot hire unless cash > 3 months of wages.
    *   *Code*: `can_afford_hire = cash > wage * 3`.
    *   *Safety*: Prevents firms from hiring workers they can't pay (Fraud).
*   **Bankruptcy**:
    *   *Rule*: If `cash < 0`, reset.
    *   *Code*: `_restructure()` resets cash to `INITIAL/2` and fires everyone.
    *   *Safety*: Prevents "Zombie Firms" with negative billions in debt. Keeps the simulation running.

## 3. Market Logic (`agent_manager.py`)
*   **Tax Collection (TDS)**:
    *   *Rule*: Income tax deducted *before* wage payment.
    *   *Code*: `net_wage = wage - tax`.
    *   *Safety*: Prevents households from spending tax money on goods and going into debt to the government.
*   **Fair Shopping**:
    *   *Rule*: Randomize shopper order.
    *   *Code*: `random.shuffle(shoppers)`.
    *   *Safety*: Prevents Household #0 from hoarding all cheap goods every month.
*   **Panic Hiring**:
    *   *Rule*: If a firm fails to hire due to low wages, it raises wages aggressively (10%).
    *   *Code*: `if failed_to_hire: wage_offer *= 1.10`.
    *   *Safety*: Ensures wages catch up to inflation/reservation wages, preventing 100% unemployment traps.
*   **Budget Commitment**:
    *   *Rule*: Firms cannot hire more workers than their *remaining* cash allows.
    *   *Code*: `committed_budget` tracker in `AgentManager`.
    *   *Safety*: Prevents firms from spending 100% of cash on wages and going bankrupt immediately.
*   **Inventory Rot**:
    *   *Rule*: 10% of unsold goods disappear.
    *   **Risk**: Floating Point Errors (e.g., Cash = -0.0000001).
    *   *Mitigation*: All checks use strict inequalities (`>`). Python floats are generally precise enough for this scale.
*   **Risk**: Hyperinflation (Prices > $1M).
    *   *Observation*: Simulation runs too fast, causing compounding inflation to explode numbers visually.
    *   *Mitigation*: Implement FPS Cap (Speed Control) in Dashboard. Future: Add "Central Bank" logic to raise interest rates if inflation > 5%.

## 4. Government Logic (`agent_manager.py`)
### 7. Government Budget Constraint
*   **Rule**: The government cannot print infinite money for UBI or Bailouts.
*   **Implementation**: `AgentManager` tracks `govt_cash`. Tax revenue adds to it. UBI/Bailouts subtract from it.
*   **Constraint**: If `govt_cash` is insufficient, UBI is reduced pro-rata. Bailouts are capped or denied.
*   **Bailout Fund**:
    *   *Rule*: Bailouts are paid from Government Cash.
    *   *Code*: `if govt_cash > bailout_cost: pay_bailout()`.
    *   *Safety*: If the government is broke, firms are allowed to fail (or revived with minimal "Startup Grant" instead of massive bailout). `PRICE_STICKINESS` slows down the spiral, giving the RL agent time to react (e.g., lower taxes).

### 8. Market Fairness (Anti-Monopoly)
*   **Rule**: No single firm should capture the entire labor or goods market purely due to iteration order or perfect information.
*   **Implementation**:
    *   **Labor Market**: `hiring_firms` are shuffled every step. This prevents Firm 0 from always getting the first pick of workers.
    *   **Goods Market**: Consumers use **Limited Search**. Instead of checking all firms and picking the absolute cheapest (Winner-Takes-All), they check a random sample of 3 firms and pick the cheapest among them. This simulates imperfect information and local availability, allowing smaller/slightly more expensive firms to survive.
*   **Dynamic Startup Capital**:
    *   **Rule**: When a firm resets (bankruptcy), it must be given enough cash to compete in the *current* economy, not the *initial* economy.
    *   **Implementation**: `_restructure()` logic (pending AgentManager update) or simply soft-resetting price/wage to 80% of previous values instead of hard reset to 10.0/100.0. This prevents the "Death Spiral" where new firms are born too poor to hire anyone.

### 9. Labor Market Friction (Contracts)
*   **Rule**: Workers cannot switch jobs instantly every month.
*   **Implementation**:
    *   **Contracts**: When hired, a worker is locked for 6 months (`contract_remaining`).
    *   **Churn**: Only unemployed workers or those with expired contracts enter the job market.
    *   **Effect**: Prevents a single firm from capturing 100% of the workforce in a single step just by offering $1 more. Stabilizes firm sizes.

### 10. Production Efficiency (Diminishing Returns)
*   **Rule**: Infinite scaling is inefficient without infrastructure upgrades.
*   **Implementation**:
    *   **Formula**: `Production = Productivity * (Total Skill ^ 0.9)`.
    *   **Effect**: A firm with 100 workers is less than 10x as productive as a firm with 10 workers. This creates a natural "soft cap" on firm size, encouraging a multi-firm ecosystem rather than a single monopoly.

### 11. Firm Growth Limits (Tiers)
*   **Rule**: Firms cannot grow indefinitely without investing in infrastructure.
*   **Implementation**:
    *   **Tiers**: 4 Levels (Startup, Small Biz, Medium, Corp) with strict **Max Employee** caps (5, 20, 50, 200).
    *   **Upgrades**: Firms must pay a significant cost to upgrade tiers.
    *   **Inflation Adjustment**: Upgrade costs scale with the price level to remain relevant, but are dampened using a square root function (`cost * sqrt(price_ratio)`). This allows firms to "catch up" to inflation, making upgrades achievable even in high-inflation environments (preventing the "Startup Trap").
    *   **Safety Buffer**: Firms only upgrade if they have **2x** the upgrade cost in cash, preventing immediate bankruptcy after investment.
    *   **Effect**: Prevents "Instant Monopolies". Firms must prove profitability and accumulate capital before they can hire more workers.

## 5. Recent Stability Patches (Post-Audit)
*   **Inventory Cap & Spoilage**:
    *   *Rule*: Households cannot hoard infinite goods.
    *   *Code*: `MAX_INVENTORY = 24.0`. Any inventory above this is discarded (spoiled).
    *   *Safety*: Prevents hoarding behavior where households convert all cash to goods, causing artificial scarcity and high prices. Forces cash savings.
*   **Productivity Adjustment**:
    *   *Rule*: Supply must match Demand.
    *   *Change*: Reduced `AVG_PRODUCTIVITY` from 300.0 to 10.0.
    *   *Reason*: Previous value caused massive oversupply (150x demand), leading to inventory gluts and zero revenue.
*   **Initial Capital Injection**:
    *   *Rule*: Firms need a runway.
    *   *Change*: Increased `INITIAL_CASH_FIRM` from 20k to 100k.
    *   *Reason*: Allows firms to survive the initial "hiring phase" where they pay wages but have no product to sell yet.
*   **Overhead Reduction**:
    *   *Rule*: Fixed costs shouldn't kill small businesses.
    *   *Change*: Reduced overheads (Tier 1: 500 -> 100).
    *   *Reason*: High overheads were causing "infant mortality" for new firms before they could become profitable.
