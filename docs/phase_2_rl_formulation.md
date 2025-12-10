# Phase 2: RL Formulation - Detailed Specification

This document defines the interface between the Economic Model and the Reinforcement Learning Agent. It translates economic variables into tensors.

## 1. The Agent
*   **Identity**: The Central Government / Central Bank.
*   **Goal**: Optimize long-term social welfare (defined by the Reward Function).

## 2. Observation Space (The State)
The agent needs a comprehensive snapshot of the economy. We must normalize these values (usually 0-1 or -1 to 1) for Neural Network stability.

### 2.1 Macro-Economic Indicators (Vector of Floats)
*   `gdp_growth`: (Current GDP - Last GDP) / Last GDP.
*   `inflation_rate`: (Current CPI - Last CPI) / Last CPI.
*   `unemployment_rate`: Unemployed / Total Workforce.
*   `interest_rate`: Current central bank rate.
*   `tax_revenue`: Total tax collected / GDP.
*   `government_debt_ratio`: Debt / GDP.

### 2.2 Social Indicators
*   `gini_coefficient`: Measure of wealth inequality (0 = perfect equality, 1 = perfect inequality).
*   `avg_household_wealth`: Mean wealth.
*   `poverty_rate`: % of households below poverty line.

### 2.3 Market Signals
*   `avg_price`: Average price of goods.
*   `avg_wage`: Average wage.
*   `inventory_turnover`: % of goods sold vs produced.

**Total State Dimension**: Approx 15-20 continuous variables.

## 3. Action Space (The Controls)
The agent outputs a vector of continuous values, which are mapped to policy rates.

### 3.1 Continuous Actions (Box Space)
*   `income_tax_rate`: Range [0.0, 0.8] (0% to 80%).
*   `corporate_tax_rate`: Range [0.0, 0.8].
*   `sales_tax`: Range [0.0, 0.3].
*   `interest_rate`: Range [0.0, 0.2] (Central bank lending rate).
*   `ubi_amount`: Range [0.0, 100.0] (Universal Basic Income payout per step).

### 3.2 Constraints
*   We must clip actions to realistic bounds to prevent the AI from setting 100% tax and crashing the simulation immediately during exploration.

## 4. Reward Function (The Objective)
The most critical component. It defines "Good" behavior.

### 4.1 Component Rewards
*   $R_{GDP}$: $+1 \times \text{GDP Growth}$ (Encourage growth).
*   $R_{Stability}$: $-1 \times |\text{Inflation} - 0.02|$ (Penalize deviation from 2% inflation target).
*   $R_{Equality}$: $-2 \times \text{Gini Coefficient}$ (Penalize high inequality).
*   $R_{Employment}$: $-1 \times \text{Unemployment Rate}$ (Penalize unemployment).

### 4.2 The Composite Formula
$$ R_{total} = w_1 R_{GDP} + w_2 R_{Stability} + w_3 R_{Equality} + w_4 R_{Employment} $$

*   **Curriculum Learning**:
    *   *Stage 1*: Train only on $R_{GDP}$ (Learn to function).
    *   *Stage 2*: Add $R_{Stability}$ (Learn to be stable).
    *   *Stage 3*: Add $R_{Equality}$ (Learn to be fair).

## 5. Episode Structure
*   **Step**: 1 Month.
*   **Episode Length**: 120 Steps (10 Years) or 240 Steps (20 Years).
*   **Termination Conditions**:
    *   Economic Collapse (GDP drops by 50%).
    *   Hyperinflation (Inflation > 50%).
    *   Revolution (Happiness < Threshold - optional).
