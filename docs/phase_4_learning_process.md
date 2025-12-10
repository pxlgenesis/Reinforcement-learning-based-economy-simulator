# Phase 4: Learning Process - Detailed Specification

This document outlines how we train the RL agent, including algorithm selection, hyperparameter tuning, and the training loop.

## 1. Algorithm Selection
*   **Primary Choice**: **PPO (Proximal Policy Optimization)**.
    *   *Why?* It is the industry standard for continuous control problems. It is robust, easy to tune, and prevents the "catastrophic forgetting" often seen in other algorithms.
*   **Library**: `Stable Baselines3` (SB3).
    *   Provides a reliable implementation of PPO.
    *   Easy integration with TensorBoard.

## 2. Training Configuration

### 2.1 Hyperparameters (Initial Guesses)
*   `learning_rate`: 3e-4 (Standard Adam default).
*   `n_steps`: 2048 (Number of steps to run before updating).
*   `batch_size`: 64.
*   `gamma` (Discount Factor): 0.99 (We care about long-term stability).
*   `ent_coef` (Entropy): 0.01 (Encourage exploration early on).

### 2.2 Network Architecture
*   **Policy Network (Actor)**: 2 layers of 64 units (`[64, 64]`).
*   **Value Network (Critic)**: 2 layers of 64 units (`[64, 64]`).
*   *Input*: The 15-20 normalized observation variables.
*   *Output*: The 5 continuous action variables.

## 3. Training Strategy

### 3.1 Baseline Establishment
Before training, we run the simulation with a **Random Agent** and a **Fixed Rule Agent** (e.g., always keep tax at 20%).
*   This gives us a "Score to Beat".
*   If the RL agent performs worse than the Fixed Rule Agent, something is wrong.

### 3.2 Curriculum Learning (Phased Difficulty)
1.  **Phase 1: Survival**:
    *   Reward: Only GDP + Survival.
    *   Goal: Prevent the economy from crashing in the first 10 years.
2.  **Phase 2: Stability**:
    *   Reward: Add Inflation penalty.
    *   Goal: Grow without hyperinflation.
3.  **Phase 3: Utopia**:
    *   Reward: Add Inequality penalty.
    *   Goal: The complex balancing act.

## 4. Experiment Tracking
*   We will use **TensorBoard** to track:
    *   `rollout/ep_rew_mean`: Average reward per episode.
    *   `train/loss`: Network loss.
    *   `economy/gdp`: Custom metric logged via Callback.
    *   `economy/gini`: Custom metric logged via Callback.

## 5. Saving & Checkpointing
*   Save the model every 10,000 steps.
*   Keep the "Best Model" (highest mean reward).
*   This allows us to resume training if it crashes or if we want to tweak parameters.
