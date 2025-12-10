# Phase 3: Simulation Architecture - Detailed Specification

This document details the software engineering architecture, data structures, and technical implementation plan.

## 1. Tech Stack
*   **Language**: Python 3.10+.
*   **Core Logic**: Pure Python classes for Agents (for flexibility).
*   **Randomness Control**: To ensure PPO (Phase 4) can learn effectively despite the noise of an Agent-Based Model, we must support **Fixed Seeding**. This allows the AI to replay the "same" economic scenario to see if its policy changes made a difference.
*   **Data Handling**: `NumPy` for vectorized operations (if scaling > 1000 agents), `Pandas` for logging history.
*   **RL Interface**: `Gymnasium` (inheriting from `gym.Env`).

## 2. Class Hierarchy

### 2.1 `EconomyEnv(gym.Env)`
The main entry point.
*   **Methods**:
    *   `__init__`: Setup spaces and config.
    *   `reset()`: Re-initialize agents and clear history.
    *   `step(action)`: Execute one month. Returns `(observation, reward, terminated, truncated, info)`.
    *   `render()`: (Optional) Print stats or update a live graph.

### 2.2 `AgentManager`
Handles the population of households and firms.
*   **Members**:
    *   `households`: List[`Household`].
    *   `firms`: List[`Firm`].
*   **Methods**:
    *   `execute_production()`: Trigger all firms to produce.
    *   `execute_labor_market()`: Match workers to jobs.
    *   `execute_consumption()`: Trigger households to buy.
    *   `collect_taxes(rates)`: Deduct money from agents.

### 2.3 `Household` & `Firm` Classes
Simple data containers with `step()` methods containing their behavioral logic.

## 3. Data Flow & State Management
*   **Global State Dictionary**: A central dictionary or Data Class `EconomyState` that holds current macro stats. This prevents recalculating GDP multiple times per step.
    ```python
    @dataclass
    class EconomyState:
        gdp: float
        inflation: float
        avg_wage: float
        # ...
    ```

## 4. Performance Optimization
*   **Bottleneck**: The `execute_consumption` loop where every household checks prices.
*   **Solution**:
    *   If N_Households is small (< 500), simple loops are fine.
    *   If N_Households is large (> 1000), use Matrix operations.
        *   *Example*: Create a Price Matrix (Firms) and Budget Vector (Households) and use masking to determine purchases.

## 5. Directory Structure
```
economy_sim/
├── envs/
│   ├── __init__.py
│   ├── economy_env.py      # Main Gym Environment
│   └── components/
│       ├── household.py    # Household logic
│       ├── firm.py         # Firm logic
│       └── market.py       # Matching logic
├── agents/
│   ├── rule_based.py       # Heuristics for non-RL agents
├── utils/
│   ├── metrics.py          # Calculation of Gini, GDP, etc.
│   └── logger.py           # Data recording
## 6. Launcher Architecture
To unify the Python Simulation, RL Training, and React Frontend, we will use a single entry point.
*   **Location**: `launcher/launcher.py`
*   **Role**: Process Orchestrator.
*   **Features**:
    *   `python launcher.py --train`: Starts PPO training (Headless).
    *   `python launcher.py --sim`: Runs a visual simulation (starts FastAPI backend + Next.js frontend).
    *   **Graceful Shutdown**: Handles `Ctrl+C` to kill both the Python server and the Node.js frontend process cleanly.

