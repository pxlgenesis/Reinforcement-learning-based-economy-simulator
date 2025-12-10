# Economy Reinforcement Learning Simulator

An advanced Agent-Based Model (ABM) economy simulation where a Reinforcement Learning (RL) agent acts as the government to optimize economic stability and prosperity.

## 🚀 Project Overview

This project simulates a closed economy consisting of **Households** and **Firms**. An AI agent (trained using PPO) controls fiscal and monetary policy to achieve sustainable economic growth while minimizing inequality and unemployment.

### Key Features
*   **Agent-Based Modeling**:
    *   **Households**: Work, consume, save, and learn skills.
    *   **Firms**: Produce goods, set prices, hire/fire employees, and manage inventory.
*   **Market Mechanics**:
    *   **Labor Market**: Decentralized matching based on wage offers.
    *   **Goods Market**: Imperfect competition where households shop for the best prices.
*   **Reinforcement Learning**:
    *   **Agent**: Acts as the Central Bank/Government.
    *   **Actions**: Sets Income Tax, Corporate Tax, and Universal Basic Income (UBI).
    *   **Observations**: GDP, Inflation, Unemployment, Gini Coefficient, etc.
    *   **Algorithm**: Proximal Policy Optimization (PPO).
*   **Real-time Visualization**:
    *   A Next.js-based dashboard to monitor the economy in real-time.

## 📂 Project Structure

```
├── economy_sim/        # Core Python package for the simulation
│   ├── envs/           # Gym environments and agent logic (Firms, Households)
│   ├── training/       # RL training scripts (PPO)
│   └── launcher/       # Simulation launcher
├── frontend/           # Next.js web dashboard for visualization
├── models/             # Saved trained RL models
├── docs/               # Detailed documentation and architectural plans
└── tests/              # Unit and stability tests
```

## 🛠️ Installation & Setup

### 1. Backend (Simulation)

Prerequisites: Python 3.8+

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend (Dashboard)

Prerequisites: Node.js 18+

```bash
cd frontend
npm install
```

## 🏃‍♂️ Usage

### Running the Simulation
To run the simulation with the trained model and start the API server:

```bash
python -m economy_sim.launcher.launcher
```

### Running the Dashboard
In a separate terminal:

```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the simulation dashboard.

### Training the Agent
To retrain the RL agent:

```bash
python -m economy_sim.training.train_ppo
```

## 📚 Documentation

Detailed documentation can be found in the `docs/` directory:
*   [System Architecture](docs/system_architecture.md)
*   [Economic Model](docs/phase_1_economic_model.md)
*   [RL Formulation](docs/phase_2_rl_formulation.md)

## 📄 License

[MIT License](LICENSE)
