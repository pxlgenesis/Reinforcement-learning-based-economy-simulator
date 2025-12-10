# System Architecture

This document outlines the high-level architecture of the Economy Reinforcement Simulator, detailing the interaction between the Reinforcement Learning (RL) Agent and the Economic Environment.

## Workflow Description

1.  **RL Agent (The Brain)**
    *   **Input**: Receives the current `State` (Observation) from the environment, including macro indicators (GDP, Inflation) and micro aggregates (Avg Wage, Unemployment).
    *   **Processing**: The PPO (Proximal Policy Optimization) model processes this state to determine the optimal policy.
    *   **Output**: Emits an `Action` vector (Income Tax Rate, Corporate Tax Rate, UBI Level).

2.  **Economy Environment (The Simulation)**
    *   **Step 1: Policy Application**: The Agent's tax and UBI rates are applied to the government logic.
    *   **Step 2: Market Interactions**:
        *   **Firms**: Produce goods, hire workers (Labor Market), and set prices/wages.
        *   **Households**: Work (Labor Supply), consume goods (Goods Market), and pay taxes.
    *   **Step 3: Physics & Rules**: The simulation enforces constraints such as diminishing returns, contract durations, and bankruptcy rules.

3.  **Reward System**
    *   Calculates a scalar score based on the health of the economy (e.g., rewarding GDP growth, penalizing high inflation/unemployment).
    *   This `Reward` is fed back to the Agent to reinforce beneficial behaviors.

4.  **Frontend Dashboard**
    *   Connects via WebSocket to the Simulation.
    *   Visualizes the real-time state of the economy (KPIs, Charts, Tables) for human monitoring.
