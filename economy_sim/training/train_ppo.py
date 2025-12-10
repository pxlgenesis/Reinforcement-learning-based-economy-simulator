import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from economy_sim.envs.economy_env import EconomyEnv
from economy_sim.config import RANDOM_SEED

def make_env(rank: int, seed: int = 0):
    """
    Utility function for multiprocessed env.
    """
    def _init():
        env = EconomyEnv()
        env.reset(seed=seed + rank)
        return env
    return _init

def train():
    # Create directories
    models_dir = "models/ppo"
    logs_dir = "logs"
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Parallel environments
    # Use SubprocVecEnv for true parallelism on CPU
    # num_cpu = 4  # Adjust based on your i9
    # env = SubprocVecEnv([make_env(i, RANDOM_SEED) for i in range(num_cpu)])
    
    # For debugging/initial run, use DummyVecEnv (Single Process)
    env = DummyVecEnv([make_env(0, RANDOM_SEED)])

    # Initialize PPO Agent
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        tensorboard_log=logs_dir,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        device="cuda" # Use RTX 4070
    )

    # Save a checkpoint every 10,000 steps
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path=models_dir,
        name_prefix="economy_ppo"
    )

    print("Starting PPO Training...")
    print(f"Device: {model.device}")
    
    # Train for 100,000 steps (approx 300 episodes)
    model.learn(total_timesteps=100000, callback=checkpoint_callback)
    
    # Save final model
    model.save(f"{models_dir}/economy_ppo_final")
    print("Training Complete. Model saved.")
    
    # Append to log file
    with open("training_summary_log.txt", "a") as f:
        f.write(f"\n\nTraining Run Completed.\nTotal Timesteps: 100,000\nDevice: {model.device}\n")

if __name__ == "__main__":
    train()
