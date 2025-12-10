# Economic Model Specification

This document defines the "Physics Engine" of the simulation, detailing the entities, their attributes, and the immutable rules governing their interactions.

## 1. Core Philosophy: Agent-Based Model (ABM)
The simulation models individual economic actors. Macroeconomic trends emerge from their micro-interactions.
*   **Time Scale**: Discrete steps (1 Step = 1 Month).
*   **Currency**: Credits (infinitely divisible).

## 2. Entities

### 2.1 Households (Consumers & Workers)
*   **Role**: Work, consume, save, and acquire skills.
*   **Key Attributes**:
    *   `cash`: Current liquid assets.
    *   `labor_skill`: Productivity multiplier (0.5 - 2.0). Increases with employment, decays with unemployment.
    *   `reservation_wage`: Minimum acceptable wage.
*   **Behavior**:
    *   **Consumption**: Must spend a `subsistence_cost` monthly. Discretionary spending occurs if surplus cash exists.
    *   **Labor**: Accepts job offers where `wage > reservation_wage`.

### 2.2 Firms (Producers & Employers)
*   **Role**: Produce goods, set prices, and manage employment.
*   **Key Attributes**:
    *   `cash`: Capital for operations.
    *   `inventory`: Unsold goods.
    *   `price`: Current selling price.
    *   `wage_offer`: Current wage for new hires.
*   **Behavior**:
    *   **Production**: $Output = A \times (Labor)^\alpha$.
    *   **Pricing**: Adjusts based on inventory levels (High inventory $\rightarrow$ Lower price). Constrained to $\pm 5\%$ change per step.
    *   **Hiring**: Posts vacancies if profitable and cash reserves allow (3-month buffer required).
    *   **Bankruptcy**: If `cash < 0`, the firm is restructured (debts wiped, capital reset).

### 2.3 Government (The Agent)
*   **Role**: The central authority controlled by the RL model.
*   **Attributes**: `treasury` (tax revenue), `debt`.

## 3. Market Mechanisms

### 3.1 Labor Market (Decentralized Matching)
1.  Unemployed households search for jobs.
2.  Firms post vacancies with wage offers.
3.  Households accept the highest offer meeting their reservation wage.

### 3.2 Goods Market (Imperfect Competition)
1.  Firms set prices and quantities.
2.  Households survey a subset of firms and purchase from the cheapest option.
3.  Transactions transfer cash to firms and goods to households.

## 4. Execution Cycle (Per Step)
1.  **Policy Update**: Government sets tax rates and UBI.
2.  **Production**: Firms produce goods and pay wages.
3.  **Labor Market**: Hiring and firing occurs.
4.  **Consumption**: Households buy goods; firms earn revenue.
5.  **Fiscal Event**: Taxes collected; subsidies/UBI paid.
6.  **Maintenance**: Inventory decay and skill updates.
