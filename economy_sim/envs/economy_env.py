import gymnasium as gym
import numpy as np
from gymnasium import spaces
from economy_sim.envs.components.agent_manager import AgentManager
from economy_sim.config import EPISODE_LENGTH

class EconomyEnv(gym.Env):
    """
    The Gym Environment for the Economy Simulation.
    Action Space: Continuous [Income Tax, Corp Tax, UBI]
    Observation Space: [GDP, Inflation, Unemployment, Gini, Tax Revenue, Avg Wage, Avg Price]
    """
    
    def __init__(self):
        super(EconomyEnv, self).__init__()
        
        self.agent_manager = AgentManager()
        self.current_step = 0
        
        # Action Space:
        # 0: Income Tax Rate (0.0 - 0.8)
        # 1: Corp Tax Rate (0.0 - 0.8)
        # 2: UBI Amount (0.0 - 200.0) -> Normalized to 0-1 in action, scaled inside
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(3,), dtype=np.float32)
        
        # Observation Space:
        # 7 Metrics normalized roughly to [-1, 1] or [0, 1]
        # [Unemployment, Avg Price, Avg Wage, Tax Revenue, GDP, Gini, Subsistence Failures]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)
        
        # History for Reward Calculation
        self.last_gdp = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_manager = AgentManager() # Reset agents
        self.current_step = 0
        self.last_gdp = 0.0
        
        return self._get_observation(), {}

    def step(self, action):
        # 1. Parse Action
        income_tax = np.clip(action[0] * 0.8, 0.0, 0.8) # Scale 0-1 to 0-80%
        corp_tax = np.clip(action[1] * 0.8, 0.0, 0.8)
        ubi = action[2] * 200.0 # Scale 0-1 to 0-200 credits
        
        tax_rates = {
            "income_tax": income_tax,
            "corp_tax": corp_tax,
            "ubi": ubi
        }
        
        # 2. Run Simulation Step
        self.agent_manager.step(tax_rates)
        self.current_step += 1
        
        # 3. Get Observation
        obs = self._get_observation()
        
        # 4. Calculate Reward
        reward = self._calculate_reward(obs)
        
        # 5. Check Termination
        terminated = False
        truncated = self.current_step >= EPISODE_LENGTH
        
        # Crash condition: If unemployment > 90% (Collapse)
        # Relaxed: Only crash if it persists? For now, let's keep it strict but rely on Bailout.
        # Actually, if Bailout happens in AgentManager.step(), unemployment might still be high 
        # until the NEXT step when they hire.
        # Let's allow 1 step of chaos.
        stats = self.agent_manager.get_market_stats()
        if stats["unemployment"] > 0.95 and self.current_step > 5:
             # Only terminate if we are past warmup and it's total collapse
             # But wait! Bailout spawns firms, but they need time to hire.
             # Let's just penalize heavily but NOT terminate, to let RL learn to recover.
             # terminated = True 
             reward -= 50.0 # Heavy penalty
        
        info = {
            "gdp": self.last_gdp,
            "unemployment": stats["unemployment"],
            "tax_revenue": stats["tax_revenue"]
        }
        
        return obs, reward, terminated, truncated, info

    def _get_observation(self):
        stats = self.agent_manager.get_market_stats()
        
        # Real Observation Vector
        obs = np.array([
            stats["unemployment"],
            stats["avg_price"],
            stats["avg_wage"],
            stats["tax_revenue"],
            stats["gdp"], 
            stats["gini"],
            stats["subsistence_failures"]
        ], dtype=np.float32)
        
        # Sanitize (Replace NaN/Inf with 0)
        return np.nan_to_num(obs, nan=0.0, posinf=1e6, neginf=-1e6)

    def _calculate_reward(self, obs):
        # R = GDP_Growth - Unemployment - Inflation_Instability
        # Simplified for first pass
        unemployment = obs[0]
        
        reward = 0.0
        reward -= (unemployment * 10.0) # Penalize unemployment heavily
        
        return reward
