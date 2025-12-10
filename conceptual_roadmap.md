# Master Roadmap: Economy Reinforcement Learning Simulation

This is the finalized, "Battle-Tested" plan for building the simulation. It incorporates all stability safeguards, efficiency metrics, and architectural decisions made during the design phase.

## Phase 1: The Economic Engine (Physics)
**Goal**: Build a stable Agent-Based Model (ABM) that doesn't crash on its own.

### 1.1 Entities
*   **Households (N=100)**:
    *   *Logic*: Work, Consume, Save.
    *   *Stability Rule*: **Subsistence Consumption**. Must spend `SUBSISTENCE_COST` to survive.
    *   *Stability Rule*: **Wage Floor**. Will not work for less than `SUBSISTENCE_COST`.
    *   *Dynamics*: **Skill Learning**. Employed = Skill Up (1%/yr). Unemployed = Skill Decay.
*   **Firms (N=10)**:
    *   *Logic*: Produce, Price, Hire/Fire.
    *   *Stability Rule*: **Sticky Prices**. Max price change $\pm 5\%$ per step.
    *   *Stability Rule*: **Hiring Budget**. Cannot hire without 3 months of cash buffer.
    *   *Stability Rule*: **Inventory Depreciation**. Unsold goods rot (10% per month) to force continuous production.
    *   *Safety*: **Restructuring**. Bankrupt firms are reset (debt wiped) but logged as failures.

### 1.2 Market Mechanics
*   **Labor Market**: Decentralized matching. Highest wage offer wins.
*   **Goods Market**: Imperfect competition. Households check 3 random firms and buy cheapest.

---

## Phase 2: The RL Interface (API)
**Goal**: Translate the economy into a format the AI can understand and control.

### 2.1 Observation Space (Normalized)
*   **Macro**: GDP Growth, Inflation, Unemployment.
*   **Social**: Gini Coefficient (Inequality), Poverty Rate (Subsistence Failures).
*   **Fiscal**: Tax Revenue, Debt/GDP Ratio.
*   *Crucial*: All inputs normalized to range `[-1, 1]` or `[0, 1]` for Neural Net stability.

### 2.2 Action Space (Continuous)
*   **Taxes**: Income Tax, Corporate Tax.
*   **Monetary**: Interest Rate.
*   **Welfare**: UBI (Universal Basic Income) Amount.

### 2.3 Reward Function
*   **Objective**: Sustainable Prosperity.
*   **Formula**: $R = \text{Norm}(GDP) - w_1 \times \text{Inequality} - w_2 \times \text{InflationInstability} - w_3 \times \text{Unemployment}$.
*   *Note*: Rewards must be scaled so one term doesn't dominate.

---

## Phase 3: Architecture & Implementation
**Goal**: Build the code infrastructure.

### 3.1 Tech Stack
*   **Language**: Python 3.10+
*   **Engine**: `Gymnasium` (Custom Env).
*   **Agents**: Pure Python Classes.
*   **Frontend**: Next.js (React) + TailwindCSS + Shadcn UI.
*   **Backend**: FastAPI (WebSockets).

### 3.2 Execution Flow
1.  **Warm-Up**: Run 50 steps with a "Fixed Safe Policy" to stabilize the economy.
2.  **Handover**: Give control to RL Agent.
3.  **Step Loop**: Govt Action -> Production -> Labor Market -> Consumption -> Depreciation -> Logging.

### 3.3 Configuration (`config.py`)
*   `N_HOUSEHOLDS = 100`
*   `N_FIRMS = 10`
*   `SUBSISTENCE_COST` < `AVG_PRODUCTIVITY` (Crucial for employment).

### 3.4 Launcher Architecture
# Master Roadmap: Economy Reinforcement Learning Simulation

This is the finalized, "Battle-Tested" plan for building the simulation. It incorporates all stability safeguards, efficiency metrics, and architectural decisions made during the design phase.

## Phase 1: Economic Model Design [COMPLETED]
*   **Goal**: Define the rules of the game.
*   **Core Components**:
    *   **Households**: Agents that work, consume, and save. Logic: `Subsistence`, `Reservation Wage (COLA)`, `Skill Decay`.
    *   **Firms**: Agents that hire, produce, and sell. Logic: `Sticky Prices`, `Panic Hiring`, `Bankruptcy/Bailout`.
    *   **Government**: Collects taxes (Income/Corporate) and distributes UBI.
    *   **Market**: `AgentManager` handles labor/goods matching and `Fair Shopping` order.

## Phase 2: RL Formulation [COMPLETED]
*   **Goal**: Define how the AI interacts with the economy.
*   **State Space (Observation)**: `[Unemployment, Avg Price, Avg Wage, Tax Revenue, GDP, Gini, Subsistence Failures]`.
*   **Action Space**: `[Income Tax Rate, Corp Tax Rate, UBI Amount]`.
*   **Reward Function**: `GDP Growth - Penalty(Unemployment) - Penalty(Instability)`.

## Phase 3: Simulation Architecture [COMPLETED]
*   **Goal**: Build the engine.
*   **Tech Stack**: Python 3.10+, NumPy, Pandas.
*   **Structure**:
    *   `economy_sim/envs/`: Gymnasium Environment.
    *   `economy_sim/components/`: Agent classes.
    *   `launcher/`: Entry point (`launcher.py`).
*   **Stability**: Implemented `Budget Commitment`, `Stronger Bailout`, and `Sanitized Observations` to prevent crashes.

## Phase 4: Learning Process [COMPLETED]
*   **Goal**: Train the AI.
*   **Algorithm**: PPO (Proximal Policy Optimization) via `stable-baselines3`.
*   **Training**:
    *   Script: `train_ppo.py`.
    *   Device: CUDA (RTX 4070).
    *   Status: Trained for 100k steps. Agent learned to avoid collapse.

## Phase 5: Analysis & Visualization [IN PROGRESS]
*   **Goal**: See the results in real-time.
*   **Tech Stack**:
    *   **Backend**: FastAPI (`api_server.py`) with WebSockets.
    *   **Frontend**: Next.js + TailwindCSS + Shadcn UI + Recharts.
*   **Features**:
    *   Real-time Dashboard (GDP, Inflation, Unemployment).
    *   Interactive Controls (Play/Pause, Reset).
    *   **Next Steps**: Implement Speed Control and Manual/AI Toggle.

## Phase 6: Refinement & Tuning [PLANNED]
*   **Goal**: Make it realistic.
*   **Tasks**:
    *   Tune hyperparameters to prevent hyperinflation.
    *   Longer training runs (1M+ steps).
    *   Add more complex agent behaviors (Savings rates, Luxury goods).nfig.py`.
2.  **Core**: `Household` and `Firm` classes (with all stability rules).
3.  **Env**: `EconomyEnv` class (Gym interface).
4.  **Test**: Run with Random Agent (Verify no immediate crashes).
5.  **Train**: Connect PPO.
6.  **UI**: Build Dashboard (Next.js + Shadcn).
