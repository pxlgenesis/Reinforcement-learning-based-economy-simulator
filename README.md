# Economy Reinforcement Learning Simulator

## Project Overview

This project implements an Agent-Based Model (ABM) economy simulation where a Reinforcement Learning (RL) agent acts as the government. The primary objective is to optimize economic stability and prosperity through fiscal and monetary policy interventions.

The simulation consists of a closed economy with two primary agent types:
*   **Households**: Agents that work, consume goods, save money, and acquire skills over time.
*   **Firms**: Entities that produce goods, set prices, hire or fire employees based on demand, and manage inventory.

The RL agent, trained using Proximal Policy Optimization (PPO), observes macroeconomic indicators (such as GDP, inflation, unemployment, and the Gini coefficient) and takes actions to influence the economy. These actions include setting income tax rates, corporate tax rates, and Universal Basic Income (UBI) levels.

## Project Structure

*   `economy_sim/`: Contains the core Python package for the simulation, including environment definitions and agent logic.
*   `frontend/`: A Next.js web application that serves as a dashboard for real-time visualization of the simulation.
*   `models/`: Stores trained Reinforcement Learning models.
*   `docs/`: Includes detailed documentation regarding the system architecture, economic model, and RL formulation.

## Installation

### Backend (Simulation)

The simulation requires Python 3.8 or higher.

1.  Create a virtual environment:
    ```bash
    python -m venv .venv
    ```

2.  Activate the virtual environment:
    *   Windows: `.venv\Scripts\activate`
    *   Unix/MacOS: `source .venv/bin/activate`

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend (Dashboard)

The dashboard requires Node.js 18 or higher.

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install the dependencies:
    ```bash
    npm install
    ```

## Usage

### Running the Simulation

To execute the simulation using the trained model and start the API server for the dashboard:

```bash
python -m economy_sim.launcher.launcher
```

### Running the Dashboard

To start the visualization dashboard:

1.  Open a new terminal window.
2.  Navigate to the `frontend` directory.
3.  Start the development server:

```bash
npm run dev
```

4.  Access the dashboard at `http://localhost:3000` in your web browser.

### Training the Agent

To retrain the Reinforcement Learning agent:

```bash
python -m economy_sim.training.train_ppo
```

## Documentation

For further details on the implementation, refer to the documents in the `docs/` directory:
*   [System Architecture](docs/system_architecture.md)
*   [Economic Model](docs/economic_model.md)
*   [RL Formulation](docs/rl_formulation.md)

## License

This project is licensed under the MIT License.
