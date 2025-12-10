# Phase 1: Economic Model Design - Detailed Specification

This document serves as the "Physics Engine" specification for our simulation. It defines the entities, their properties, and the immutable rules of interaction.

## 1. Core Philosophy: Agent-Based Model (ABM)
We simulate individual economic actors. The macro-economy is an emergent property of their micro-interactions.
*   **Time Scale**: Discrete steps. 1 Step = 1 Month.
*   **Currency**: "Credits" (Infinite divisibility).

## 2. Entities & Attributes

### 2.1 Households (The Consumers & Workers)
*   **Population**: $N_{households}$ (e.g., 100 - 1000 initially).
*   **State Attributes**:
    *   `id`: Unique identifier.
    *   `cash`: Current money balance.
    *   `labor_skill`: Multiplier for productivity (0.5 to 2.0).
    *   `inventory`: Amount of "Goods" held (consumables).
    *   `employed_at`: ID of the Firm employing them (None if unemployed).
    *   `wage`: Current salary (if employed).
*   **Behavioral Logic (Rule-Based initially)**:
    *   **Consumption**:
        *   *Subsistence Rule*: Households MUST spend at least `subsistence_cost` per month on goods if they have cash. This ensures money circulation.
        *   *Discretionary*: Will spend $X\%$ of remaining cash on extra goods if inventory is low.
    *   **Labor**: Will accept job offers if `offered_wage > reservation_wage`.
        *   *Skill Learning*: If employed, `labor_skill` increases by 1% per year (Experience). If unemployed > 1 year, it decays by 1% (Skill Atrophy). This enables Social Mobility dynamics.
    *   **Reservation Wage**: Minimum wage they are willing to work for.
        *   *Constraint (Wage Floor)*: `reservation_wage` cannot drop below `subsistence_cost`. This prevents the "Wage-Price Spiral" where wages drop to zero.

### 2.2 Firms (The Producers & Employers)
*   **Population**: $N_{firms}$ (e.g., 10 - 50).
*   **State Attributes**:
    *   `id`: Unique identifier.
    *   `cash`: Capital available for wages/materials.
    *   `inventory`: Finished goods ready for sale.
    *   `employees`: List of Household IDs.
    *   `price`: Current selling price of their good.
    *   `wage_offer`: Current wage offered for new hires.
*   **Behavioral Logic**:
    *   **Production Function**: $Output = A \times (Labor)^\alpha$. (Simple Cobb-Douglas with Capital fixed initially).
    *   **Pricing**: If inventory piles up $\rightarrow$ lower price. If sold out $\rightarrow$ raise price.
        *   *Constraint (Sticky Prices)*: Price changes are capped at $\pm 5\%$ per step to prevent chaotic volatility.
    *   **Hiring/Firing**: If profitable $\rightarrow$ hire more. If losing money $\rightarrow$ fire or lower wages.
        *   *Constraint (Budget Check)*: Cannot post a job opening unless `cash > 3 * wage_offer`. This prevents firms from hiring workers they cannot pay.
    *   **Bankruptcy/Restructuring**: If `cash < 0`, the firm is "bailed out" or restructured. Debts are wiped, and it restarts with a small baseline capital. **Crucial**: This event must be logged as a "failure" before reset so Phase 5 analysis can track the bankruptcy rate.

### 2.3 The Government (The Environment/Agent)
*   **Role**: The "God" entity controlled by the RL Agent.
*   **State Attributes**:
    *   `treasury`: Government funds (collected from taxes).
    *   `debt`: Accumulated deficit.

## 3. Market Mechanisms

### 3.1 The Labor Market
*   **Type**: Decentralized Matching.
*   **Process**:
    1.  Unemployed Households look for jobs.
    2.  Firms with open positions post `wage_offer`.
    3.  Households accept the highest offer above their `reservation_wage`.
    4.  Contract is formed: Household is `employed_at` Firm.

### 3.2 The Goods Market
*   **Type**: Imperfect Competition.
*   **Process**:
    1.  Firms post `price` and `quantity`.
    2.  Households decide a budget for consumption.
    3.  Households survey a subset of firms (not all, simulating imperfect information) and buy from the cheapest one found.
    4.  Transaction: Cash flows Household $\rightarrow$ Firm; Goods flow Firm $\rightarrow$ Household.

## 4. The Economic Cycle (Step Execution Order)
Every `step()` call executes these phases in order:

1.  **Policy Update**: Government sets tax rates/interest rates.
2.  **Production**: Firms calculate output based on current employees.
    *   *Cost*: Firms pay wages to Households.
    *   *Output*: Firms add new goods to `inventory`.
3.  **Labor Market Dynamics**:
    *   Firms decide to hire/fire based on previous step's sales.
    *   Unemployed households seek jobs.
4.  **Consumption (Goods Market)**:
    *   Households spend wages.
    *   Firms earn revenue.
5.  **Fiscal Event**:
    *   Government collects taxes (Income Tax from Households, Corporate Tax from Firms).
    *   Government pays subsidies/UBI (if active).
6.  **Decay/Maintenance**:
    *   Households consume goods (inventory -1).
    *   Unsold goods might depreciate.

## 5. Initialization Scenarios
*   **Egalitarian Start**: Everyone has equal cash.
*   **Pareto Start**: 20% of agents have 80% of cash (Testing inequality reduction).
