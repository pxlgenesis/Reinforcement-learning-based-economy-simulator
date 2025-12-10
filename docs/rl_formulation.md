# Reinforcement Learning Formulation

This document defines the interface between the Economic Model and the Reinforcement Learning (RL) Agent, specifying the state space, action space, and reward function.

## 1. The Agent
*   **Identity**: Central Government / Central Bank.
*   **Objective**: Optimize long-term social welfare and economic stability.

## 2. Observation Space (State)
The agent observes a normalized vector (scaled to `[-1, 1]` or `[0, 1]`) representing the economy's health.

### 2.1 Macro-Economic Indicators
*   `gdp_growth`: Percentage change in GDP.
*   `inflation_rate`: Percentage change in CPI.
*   `unemployment_rate`: Unemployed population / Total workforce.
*   `tax_revenue`: Total tax collected / GDP.
*   `government_debt_ratio`: Public Debt / GDP.

### 2.2 Social Indicators
*   `gini_coefficient`: Wealth inequality measure (0 = perfect equality, 1 = perfect inequality).
*   `avg_household_wealth`: Mean wealth across population.
*   `poverty_rate`: Percentage of households below subsistence level.

### 2.3 Market Signals
*   `avg_price`: Mean price of goods.
*   `avg_wage`: Mean wage.
*   `inventory_turnover`: Ratio of goods sold to goods produced.

## 3. Action Space (Controls)
The agent outputs a continuous vector controlling fiscal and monetary policy.

*   `income_tax_rate`: [0.0, 0.8] (Household income tax).
*   `corporate_tax_rate`: [0.0, 0.8] (Firm profit tax).
*   `ubi_amount`: [0.0, 100.0] (Universal Basic Income per step).

## 4. Reward Function
The reward function guides the agent toward desirable economic states.

$$ R_{total} = w_1 R_{GDP} + w_2 R_{Stability} + w_3 R_{Equality} + w_4 R_{Employment} $$

### Components
*   **Growth ($R_{GDP}$)**: $+1 \times \text{GDP Growth}$.
*   **Stability ($R_{Stability}$)**: Penalizes deviation from target inflation (e.g., 2%).
*   **Equality ($R_{Equality}$)**: $-2 \times \text{Gini Coefficient}$.
*   **Employment ($R_{Employment}$)**: $-1 \times \text{Unemployment Rate}$.

## 5. Training Configuration
*   **Algorithm**: Proximal Policy Optimization (PPO).
*   **Step Size**: 1 Month.
*   **Episode Length**: 120 Steps (10 Years) or 240 Steps (20 Years).
*   **Termination**: Triggered by economic collapse (GDP drop > 50%) or hyperinflation.
