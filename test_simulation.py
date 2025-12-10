import numpy as np
from economy_sim.envs.economy_env import EconomyEnv

def test_sim():
    print("Initializing Economy Environment...")
    env = EconomyEnv()
    obs, _ = env.reset()
    
    print("Starting 50-step Smoke Test...")
    print(f"{'Step':<5} | {'GDP':<10} | {'Unemployment':<15} | {'Avg Price':<10} | {'Avg Wage':<10} | {'Failures':<10}")
    print("-" * 80)
    
    for i in range(50):
        # Random Action: Tax=20%, UBI=0
        action = np.array([0.25, 0.25, 0.0], dtype=np.float32) 
        
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Parse Observation (Indices from EconomyEnv)
        # [Unemployment, Avg Price, Avg Wage, Tax Revenue, GDP, Gini, Subsistence Failures]
        unemp = obs[0]
        price = obs[1]
        wage = obs[2]
        # Note: In EconomyEnv._get_observation, I put placeholders for GDP/Gini/Failures
        # I need to fix EconomyEnv to actually return them first! 
        # But let's run it to see what happens.
        
        # Access AgentManager directly for debug stats
        stats = env.agent_manager.get_market_stats()
        
        print(f"{i:<5} | {stats['gdp']:<10.2f} | {stats['unemployment']:<15.2%} | {stats['avg_price']:<10.2f} | {stats['avg_wage']:<10.2f} | {stats['subsistence_failures']:<10}")
        
        if terminated:
            print(f"CRASHED at step {i}!")
            break
            
    print("Test Complete.")

if __name__ == "__main__":
    test_sim()
